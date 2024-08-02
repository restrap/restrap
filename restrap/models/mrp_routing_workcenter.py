# -*- coding: utf-8 -*-
from odoo import fields, models


class MrpRoutingWorkCenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    sewing_operation = fields.Boolean(string="Sewing Operation")