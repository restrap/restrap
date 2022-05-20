# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    mrp_split = fields.Boolean("Manufacture Order Split")
    mrp_split_duration = fields.Float("Manufacture Order Split Duration")
    eori = fields.Char(string="EORI")


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    eori = fields.Char(string="EORI", related='company_id.eori')