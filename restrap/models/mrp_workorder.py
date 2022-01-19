# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    split_order_id = fields.Many2one('mrp.production', string="Split Order", help="A field that is used to show related MOs with the same color in work order planning Gantt view.")
