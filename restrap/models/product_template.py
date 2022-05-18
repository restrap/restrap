# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sewing_teams = fields.Many2many('mrp.workcenter', 'product_workcenter_rel', 'prod_id', 'workcenter_id',
                                    string="Available Sewing Teams")

    origin_country_id = fields.Many2one('res.country', string="Origin")
