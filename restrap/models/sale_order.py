# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    merged = fields.Boolean(string="Sale Order Merged", readonly=True, copy=False)
    priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent')], string='Priority', default='0',
                                help="Products will be reserved first for the transfers with the highest priorities.")

    total_qty = fields.Float(string="Total Units", compute='get_total_qty')

    @api.depends('order_line.product_uom_qty')
    def get_total_qty(self):
        for record in self:
            record.total_qty = sum(line.product_uom_qty for line in record.order_line.
                                   filtered(lambda l: l.product_id.type != 'service'))
