# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError


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
        # Expected duration calculated from BoM
        unit_duration = sum(line.time_cycle for line in bom.operation_ids)
        unit_per_mo = split_duration / unit_duration
        mo_total_duration = unit_duration * self.product_qty
        # Check if the current MO duration is less than split duration
        if mo_total_duration <= unit_per_mo:
            raise UserError(_("Unable to split the MO as the duration is less than split duration"))
        # Subtract current mo qty and update duration
        remaining_qty = self.product_qty - unit_per_mo
        self.product_qty = unit_per_mo
        self.workorder_ids.write({'split_order_id': self.id})
        self._onchange_product_qty()

        # Split the remaining qty
        while remaining_qty > unit_per_mo or remaining_qty > 0:
            product_qty = unit_per_mo if remaining_qty > unit_per_mo else remaining_qty
            remaining_qty -= unit_per_mo
            order = self.copy({'product_qty': product_qty})
            order._onchange_product_qty()
            order.workorder_ids.write({'split_order_id': self.id})
            refs = ["<a href=# data-oe-model=mrp.production data-oe-id=%s>%s</a>" % tuple(name_get) for name_get in
                    self.name_get()]
            message = _("This order has been created from: %s") % ','.join(refs)
            order.message_post(body=message)

        self.write({'mrp_split_done': True})




