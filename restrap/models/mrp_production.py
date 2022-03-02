# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from collections import defaultdict
import datetime

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.addons.mrp.models.mrp_production import MrpProduction
from odoo.tools import float_round
from math import ceil


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    allow_mrp_split = fields.Boolean("Split allowed?", related="company_id.mrp_split")
    mrp_split_done = fields.Boolean("Split Done?", copy=False)
    reference = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C')], string="Reference")

    def action_spilt(self):
        self.ensure_one()

        def get_max_qty(qty, split_duration):
            """
            Returns max possible qty to produce 
            """
            # Get Minimum capacity set on work centers
            min_capacity = min(self.workorder_ids.mapped('workcenter_id.capacity'))
            # Round unit_per_mo to minimum capacity
            if min_capacity > 1 and self.product_qty > min_capacity:
                qty = min_capacity * ceil(qty / min_capacity)
            estimated_duration = self._get_estimated_duration(qty)
            if estimated_duration > split_duration:
                raise UserError(_("Unable to split the order. Unit duration is more than split duration."))
            qty_produce = qty
            # If estimated duration is still less than split duraiton
            # a While loop is used to add up min cpactity
            while estimated_duration <= split_duration:
                qty += 1
                estimated_duration = self._get_estimated_duration(qty)
                if estimated_duration > split_duration:
                    break
                else:
                    qty_produce += 1

            return qty_produce

        bom = self.bom_id
        if not bom:
            return
        split_duration = self.company_id.mrp_split_duration * 60
        # Expected duration calculated from BoM
        total_duration = sum(line.duration_expected for line in self.workorder_ids)
        unit_duration = sum(line.time_cycle for line in bom.operation_ids) / bom.product_qty
        # Check if the current MO duration is less than split duration
        if total_duration <= split_duration:
            raise UserError(_("Unable to split the MO as the duration is less than split duration"))

        initial_unit_per_mo = int(split_duration / unit_duration)
        unit_per_mo = get_max_qty(initial_unit_per_mo, split_duration)

        # Subtract current mo qty and update duration
        remaining_qty = self.product_qty - unit_per_mo
        self.product_qty = unit_per_mo
        self._onchange_product_qty()
        self._onchange_move_raw()
        self.workorder_ids.write({'split_order_id': self.id})

        # Split the remaining qty
        while remaining_qty > unit_per_mo or remaining_qty > 0:
            product_qty = unit_per_mo if remaining_qty > unit_per_mo else remaining_qty
            remaining_qty -= unit_per_mo
            order = self.copy({'product_qty': product_qty, 'date_planned_start': self.date_planned_start})
            order._onchange_product_qty()
            order._onchange_move_raw()
            order.workorder_ids.write({'split_order_id': self.id})
            refs = ["<a href=# data-oe-model=mrp.production data-oe-id=%s>%s</a>" % tuple(name_get) for name_get in
                    self.name_get()]
            message = _("This order has been created from: %s") % ','.join(refs)
            order.message_post(body=message)

        self.write({'mrp_split_done': True})

    def _get_estimated_duration(self, qty):
        """
        Return MO estimated total duration for given quantity
        qty: quantity to produce
        """
        self.ensure_one()
        duration = 0
        for wo in self.workorder_ids:
            if not wo.workcenter_id:
                continue
            qty_production = self.product_uom_id._compute_quantity(qty, self.product_id.uom_id)
            cycle_number = float_round(qty_production / wo.workcenter_id.capacity, precision_digits=0, rounding_method='UP')
    
            time_cycle = wo.operation_id.time_cycle
            duration += wo.workcenter_id.time_start + wo.workcenter_id.time_stop + cycle_number * time_cycle * 100.0 / wo.workcenter_id.time_efficiency
        
        return duration

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
            if workorder.operation_id.sewing_operation and workorder.product_id.sewing_teams:
                workcenters = workorder.product_id.sewing_teams
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


