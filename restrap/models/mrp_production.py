# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import defaultdict
import datetime

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.addons.mrp.models.mrp_production import MrpProduction
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime
from odoo.tools.misc import OrderedSet, format_date


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    allow_mrp_split = fields.Boolean("Split allowed?", related="company_id.mrp_split")
    mrp_split_done = fields.Boolean("Split Done?", copy=False)
    reference = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C')], string="Reference")

    def action_spilt(self):
        self.ensure_one()
        bom = self.bom_id
        if not bom:
            return
        split_duration = self.company_id.mrp_split_duration
        # Expected duration calculated from Work Orders
        total_duration = sum(line.duration_expected for line in self.workorder_ids)
        # Check if the  MO duration is less than split duration
        if total_duration <= split_duration:
            raise UserError(_("Unable to split the MO as the duration is less than split duration"))
        unit_duration = total_duration / self.product_qty
        unit_per_mo = split_duration / unit_duration

        remaining_qty = self.product_qty - unit_per_mo
        values = [unit_per_mo]
        while remaining_qty > 0:
            product_qty = unit_per_mo if remaining_qty > unit_per_mo else remaining_qty
            remaining_qty -= product_qty
            values.append(product_qty)

        self._split_orders({self: values}, unit_per_mo)

        self.write({'mrp_split_done': True})

    def _split_orders(self, amounts, unit_per_mo):
        """ Splits productions into productions smaller quantities to produce, i.e. creates
        its backorders. Same functionaloty as _split_productions()
        :param dict amounts: a dict with a production as key and a list value containing
        the amounts each production split should produce including the original production,
        e.g. {mrp.production(1,): [3, 2]} will result in mrp.production(1,) having a product_qty=3
        and a new backorder with product_qty=2.
        """

        backorder_vals_list = []
        initial_qty_by_production = {}
        split_qty = 0
        # Create the backorders.
        for production in self:
            initial_qty_by_production[production] = production.product_qty
            production.name = self._get_name_backorder(production.name, production.backorder_sequence)
            production.product_qty = amounts[production][0]
            split_qty += production.product_qty
            backorder_vals = production.copy_data()[0]
            backorder_qtys = amounts[production][1:]

            for qty_to_backorder in backorder_qtys:
                backorder_vals_list.append(dict(
                    backorder_vals,
                    product_qty=qty_to_backorder
                ))

        backorders = self.env['mrp.production'].create(backorder_vals_list)

        # Handle remaining qty after rounding
        for backorder in backorders:
            split_qty += backorder.product_qty
        remaining_qty = initial_qty_by_production[production] - split_qty
        remaining_backorder_qty = []
        while remaining_qty > 0:
            product_qty = unit_per_mo if remaining_qty > unit_per_mo else remaining_qty
            remaining_qty -= product_qty
            remaining_backorder_qty.append(product_qty)

        remaining_backorder_vals_list = []
        for qty_to_backorder in remaining_backorder_qty:
            remaining_backorder_vals_list.append(dict(
                backorder_vals,
                product_qty=qty_to_backorder
            ))
        remaining_backorders = self.env['mrp.production'].create(remaining_backorder_vals_list)

        backorders |= remaining_backorders


        index = 0
        production_to_backorders = {}
        production_ids = OrderedSet()
        for production in self:
            number_of_backorder_created = len(backorders)
            production_backorders = backorders[index:index + number_of_backorder_created]
            production_to_backorders[production] = production_backorders
            production_ids.update(production.ids)
            production_ids.update(production_backorders.ids)
            index += number_of_backorder_created

        # Split the `stock.move` among new backorders.
        new_moves_vals = []
        moves = []
        for production in self:
            for move in production.move_raw_ids:
                if move.additional:
                    continue
                unit_factor = move.product_uom_qty / initial_qty_by_production[production]
                initial_move_vals = move.copy_data()[0]
                move.product_uom_qty = production.product_qty * unit_factor

                for backorder in production_to_backorders[production]:
                    move_vals = dict(
                        initial_move_vals,
                        product_uom_qty=backorder.product_qty * unit_factor
                    )
                    if move.raw_material_production_id:
                        move_vals['raw_material_production_id'] = backorder.id
                    else:
                        move_vals['production_id'] = backorder.id
                    new_moves_vals.append(move_vals)
                    moves.append(move)
        self.env['stock.move'].create(new_moves_vals)

        # We need to adapt `duration_expected` on both the original workorders and their
        # backordered workorders. To do that, we use the original `duration_expected` and the
        # ratio of the quantity produced and the quantity to produce.
        for production in self:
            initial_qty = initial_qty_by_production[production]
            bo = production_to_backorders[production]

            # Adapt duration
            for workorder in (production | bo).workorder_ids:
                workorder.duration_expected = workorder.duration_expected * workorder.production_id.product_qty / initial_qty

        # Update split order in backorder workorders
        backorders.mapped('workorder_ids').write({'split_order_id': self.id})
        # Add original order on split orders chatter
        refs = ["<a href=# data-oe-model=mrp.production data-oe-id=%s>%s</a>" % tuple(name_get) for name_get in
                self.name_get()]
        message = _("This order has been created from: %s") % ','.join(refs)
        for order in backorders:
            order.message_post(body=message)
        return self.env['mrp.production'].browse(production_ids)

    def _plan_workorders(self, replan=False):
        """
        Overriding _plan_workorders() method as the change to alternative workcenters needs to be done before WO's are planned
        Remaining code was kept the same
        """
        self.ensure_one()

        if not self.workorder_ids:
            return
        # Schedule all work orders (new ones and those already created)
        qty_to_produce = max(self.product_qty - self.qty_produced, 0)
        qty_to_produce = self.product_uom_id._compute_quantity(qty_to_produce, self.product_id.uom_id)
        start_date = max(self.date_planned_start, datetime.datetime.now())
        if replan:
            workorder_ids = self.workorder_ids.filtered(lambda wo: wo.state in ('pending', 'waiting', 'ready'))
            # We plan the manufacturing order according to its `date_planned_start`, but if
            # `date_planned_start` is in the past, we plan it as soon as possible.
            workorder_ids.leave_id.unlink()
        else:
            workorder_ids = self.workorder_ids.filtered(lambda wo: not wo.date_planned_start)
        for workorder in workorder_ids:
            # If product contains alternative sewing teams then use those as alternative workcenters
            if workorder.product_id.sewing_teams:
                workcenters = workorder.workcenter_id | workorder.product_id.sewing_teams
            else:
                workcenters = workorder.workcenter_id | workorder.workcenter_id.alternative_workcenter_ids

            best_finished_date = datetime.datetime.max
            vals = {}
            for workcenter in workcenters:
                # compute theoretical duration
                if workorder.workcenter_id == workcenter:
                    duration_expected = workorder.duration_expected
                else:
                    duration_expected = workorder._get_duration_expected(alternative_workcenter=workcenter)

                from_date, to_date = workcenter._get_first_available_slot(start_date, duration_expected)
                # If the workcenter is unavailable, try planning on the next one
                if not from_date:
                    continue
                # Check if this workcenter is better than the previous ones
                if to_date and to_date < best_finished_date:
                    best_start_date = from_date
                    best_finished_date = to_date
                    best_workcenter = workcenter
                    vals = {
                        'workcenter_id': workcenter.id,
                        'duration_expected': duration_expected,
                    }

            # If none of the workcenter are available, raise
            if best_finished_date == datetime.datetime.max:
                raise UserError(_('Impossible to plan the workorder. Please check the workcenter availabilities.'))

            # Instantiate start_date for the next workorder planning
            if workorder.next_work_order_id:
                start_date = best_finished_date

            # Create leave on chosen workcenter calendar
            leave = self.env['resource.calendar.leaves'].create({
                'name': workorder.display_name,
                'calendar_id': best_workcenter.resource_calendar_id.id,
                'date_from': best_start_date,
                'date_to': best_finished_date,
                'resource_id': best_workcenter.resource_id.id,
                'time_type': 'other'
            })
            vals['leave_id'] = leave.id
            workorder.write(vals)
        self.with_context(force_date=True).write({
            'date_planned_start': self.workorder_ids[0].date_planned_start,
            'date_planned_finished': self.workorder_ids[-1].date_planned_finished
        })

    MrpProduction._plan_workorders = _plan_workorders


