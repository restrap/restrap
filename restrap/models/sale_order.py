# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    merged = fields.Boolean(string="Sale Order Merged", readonly=True, copy=False)
    priority = fields.Selection([('0', 'Normal'), ('1', 'Urgent')], string='Priority', default='0',
        help="Products will be reserved first for the transfers with the highest priorities.")
