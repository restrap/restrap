# -*- coding: utf-8 -*-
# Copyright 2020 CorTex IT Solutions Ltd. (<https://cortexsolutions.net/>)
# License OPL-1

from odoo import api, models
from odoo.tools import  float_utils, pycompat
import re


class FloatConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.float'

    @api.model
    def value_to_html(self, value, options):
        if 'qty' in options['expression'] or 'quantity' in options['expression']:

            if 'decimal_precision' in options:
                precision = self.env['decimal.precision'].precision_get(options['decimal_precision'])
            else:
                precision = options['precision']

            if precision is None:
                fmt = '%f'
            else:
                value = float_utils.float_round(value, precision_digits=precision)
                fmt = '%.{precision}f'.format(precision=precision)

            formatted = self.user_lang().format(fmt, value, grouping=True).replace(r'-', '-\N{ZERO WIDTH NO-BREAK SPACE}')

            if precision is None:
                formatted = re.sub(r'(?:(0|\d+?)0+)$', r'\1', formatted)

            return pycompat.to_text(formatted.rstrip('0').rstrip('.'))

        return super(FloatConverter, self).value_to_html(value, options)
