# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.tools import float_utils, pycompat
import re


class FloatConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.float'
    #
    # @api.model
    # def value_to_html(self, value, options):
    #     if 'decimal_precision' in options:
    #         precision = self.env['decimal.precision'].precision_get(options['decimal_precision'])
    #     else:
    #         precision = options['precision']
    #
    #     if precision is None:
    #         fmt = '%f'
    #     else:
    #         value = float_utils.float_round(value, precision_digits=precision)
    #         fmt = '%.{precision}f'.format(precision=precision)
    #
    #     formatted = self.user_lang().format(fmt, value, grouping=True).replace(r'-', '-\N{ZERO WIDTH NO-BREAK SPACE}')
    #
    #     # %f does not strip trailing zeroes. %g does but its precision causes
    #     # it to switch to scientific notation starting at a million *and* to
    #     # strip decimals. So use %f and if no precision was specified manually
    #     # strip trailing 0.
    #     if precision is None:
    #         formatted = re.sub(r'(?:(0|\d+?)0+)$', r'\1', formatted)
    #
    #     return pycompat.to_text(formatted.rstrip('0').rstrip('.'))
