# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    restrap_plan_id = fields.Many2one('restrap.mrp.plan', string="Restrap Plan", help="A field that is used to show related MOs with the same color in work order planning Gantt view.")
