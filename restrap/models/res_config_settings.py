# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mrp_split = fields.Boolean("Manufacture Order Split", related="company_id.mrp_split", readonly=False)
    mrp_split_duration = fields.Float("Manufacture Order Split Duration", related="company_id.mrp_split_duration", readonly=False)
