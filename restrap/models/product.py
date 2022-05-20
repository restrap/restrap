# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.addons.product.models.product import ProductProduct


class Product(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        """
            Stop the “Sales Description” of a product from pulling through into this field.
            The field should only have the “Product Name” and “Internal Reference”
        """
        return self.display_name

    ProductProduct.get_product_multiline_description_sale = get_product_multiline_description_sale

