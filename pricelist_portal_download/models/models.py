# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_round, format_date, get_lang


class ResPartner(models.Model):
    _inherit = "res.partner"

    allow_pricelist_download = fields.Boolean("Portal Pricelist Download")
    show_product_stock = fields.Boolean()

    @api.onchange("allow_pricelist_download")
    def allow_pricelist_download_change(self):
        if not self.allow_pricelist_download:
            self.show_product_stock = False

    def get_pricelist_rules(self, ecom_category=None):
        pricelist_id = self.property_product_pricelist
        pricelist_products = []
        if pricelist_id:
            item_ids = pricelist_id.item_ids
            for rule in item_ids:
                if rule.applied_on == "0_product_variant":
                    product_id = rule.product_id
                    if ecom_category and not product_id.public_categ_ids:
                        continue
                    if ecom_category and product_id.public_categ_ids:
                        if not set(ecom_category) & set(product_id.public_categ_ids.ids):
                            continue
                    rule_data = self.get_price_rule_data(pricelist_id, rule, product_id)
                    pricelist_products.append(rule_data)
                elif rule.applied_on == "1_product":
                    if ecom_category and not rule.product_tmpl_id.public_categ_ids:
                        continue
                    if ecom_category and rule.product_tmpl_id.public_categ_ids:
                        if not set(ecom_category) & set(rule.product_tmpl_id.public_categ_ids.ids):
                            continue
                    product_variant_ids = rule.product_tmpl_id.product_variant_ids
                    for product_id in product_variant_ids:
                        rule_data = self.get_price_rule_data(pricelist_id, rule, product_id)
                        pricelist_products.append(rule_data)

                elif rule.applied_on == "2_product_category":
                    categ_id = rule.categ_id
                    domain = [("categ_id", "child_of", categ_id.id)]
                    if ecom_category:
                        domain.append(("public_categ_ids.id", "in", ecom_category))

                    product_variant_ids = self.env["product.product"].search(domain)
                    for product_id in product_variant_ids:
                        rule_data = self.get_price_rule_data(pricelist_id, rule, product_id)
                        pricelist_products.append(rule_data)

                elif rule.applied_on == "3_global":
                    domain = []
                    if ecom_category:
                        domain.append(("public_categ_ids.id", "in", ecom_category))
                    product_variant_ids = self.env["product.product"].search([])
                    for product_id in product_variant_ids:
                        rule_data = self.get_price_rule_data(pricelist_id, rule, product_id)
                        pricelist_products.append(rule_data)

        pricelist_products = sorted(pricelist_products, key=lambda item: item['product_id'].with_context(
            display_default_code=False).display_name)
        return pricelist_products

    def get_price_rule_data(self, pricelist_id, rule, product_id):
        min_quantity = 0
        price_duration = "-"
        precision = product_id.uom_id.rounding
        if rule.min_quantity:
            min_quantity = float_round(rule.min_quantity, precision_rounding=precision)
        if rule.date_start and rule.date_end:
            price_duration = format_date(self.env, rule.date_start,
                                         lang_code=get_lang(self.env).code) + " - "
            price_duration += format_date(self.env, rule.date_end,
                                          lang_code=get_lang(self.env).code)
        else:
            if rule.date_start:
                price_duration = format_date(self.env, rule.date_start,
                                             lang_code=get_lang(self.env).code)
            if rule.date_end:
                price_duration = format_date(self.env, rule.date_end,
                                             lang_code=get_lang(self.env).code)
        if rule.date_start:
            date = rule.date_start
        else:
            date = self._context.get('date') or fields.Date.today()
            date = fields.Date.to_date(date)
            # date = False
        uom_id = False
        if rule.base == 'pricelist' and rule.base_pricelist_id:
            price_tmp = \
                rule.base_pricelist_id._compute_price_rule([(product_id, rule.min_quantity or 1, self)],
                                                           date, uom_id)[product_id.id][
                    0]  # TDE: 0 = price, 1 = rule
            price = rule.base_pricelist_id.currency_id._convert(price_tmp, pricelist_id.currency_id,
                                                                self.env.company, date, round=False)
        else:
            # if base option is public price take sale price else cost price of product
            # price_compute returns the price in the context UoM, i.e. qty_uom_id
            price = product_id.price_compute(rule.base)[product_id.id]
        price_uom = product_id.uom_id
        if price is not False:
            price = rule._compute_price(price, price_uom, product_id, quantity=rule.min_quantity or 1,
                                        partner=self)

        if rule.compute_price != 'fixed' and rule.base != 'pricelist':
            if rule.base == 'standard_price':
                cur = product_id.cost_currency_id
            else:
                cur = product_id.currency_id
            price = cur._convert(price, pricelist_id.currency_id, self.env.company, date, round=False)
        website = self.env['website'].get_current_website()
        qty = product_id.with_context(warehouse=website._get_warehouse_available()).free_qty
        if qty < 0:
            qty = 0
        return {
            "product_id": product_id,
            "min_qty": min_quantity,
            "price_duration": price_duration,
            "price": price,
            "show_product_stock": self.show_product_stock,
            "stock_on_hand": qty
        }


