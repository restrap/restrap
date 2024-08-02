# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    cutting_notes = fields.Text(string="Cutting")
    sewing_notes = fields.Text(string="Sewing")
    packing_notes = fields.Text(string="Packing")
