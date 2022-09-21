from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class Country(models.Model):
    _inherit = 'res.country'

    alias_ids = fields.One2many('res.country.alias', 'country_id', string="Country Aliases")


class CountryAlias(models.Model):
    _name = 'res.country.alias'

    _sql_constraints = [
        ('alias_name_unique', 'unique (name)', "An alias with this code already exists!"),
    ]

    name = fields.Char(string="Code", required=True)
    country_id = fields.Many2one("res.country", readonly=True)
