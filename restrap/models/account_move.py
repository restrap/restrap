# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_qty = fields.Float(string="Total Units", compute='get_total_qty')

    @api.depends('invoice_line_ids.quantity')
    def get_total_qty(self):
        for record in self:
            record.total_qty = sum(line.quantity for line in record.invoice_line_ids.
                                   filtered(lambda l: l.product_id.type != 'service'))


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_computed_name(self):
        """
            Stop the “Sales Description” of a product from pulling through into this field.
            The field should only have the “Product Name” and “Internal Reference”
        """
        self.ensure_one()
        res = super(AccountMoveLine, self)._get_computed_name()

        if self.partner_id.lang:
            product = self.product_id.with_context(lang=self.partner_id.lang)
        else:
            product = self.product_id

        if self.journal_id.type == 'sale':
            return product.display_name
        return res


