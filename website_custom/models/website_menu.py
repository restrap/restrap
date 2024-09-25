# -*- coding: utf-8 -*-

from odoo import api, fields, models


class WebsiteMenu(models.Model):
    _inherit = "website"

    allow_out_of_stock_order = fields.Boolean(
        string='Continue selling when out-of-stock',
        default=True)
