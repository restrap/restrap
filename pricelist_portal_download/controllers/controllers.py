# -*- coding: utf-8 -*-
import base64
import io

import xlsxwriter
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo import http, fields
from odoo.http import request, content_disposition
from odoo.tools import format_date, get_lang


class CustomerPortalEx(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        if 'pricelist_count' in counters:
            if partner.property_product_pricelist and partner.allow_pricelist_download:
                pricelist_count = 1
            else:
                pricelist_count = 0
            values.update({
                'pricelist_count': pricelist_count,
            })
        return values

    @http.route(['/my/product-pricelist'], type='http', auth="user", website=True)
    def portal_my_product_pricelist(self, **kw):
        partner = request.env.user.partner_id
        if partner.property_product_pricelist and partner.allow_pricelist_download:
            categories = request.env["product.public.category"].search_read([], ["id", "name"])
            values = {
                "page_name": "product_pricelist",
                "ecom_categories": categories
            }
            return request.render("pricelist_portal_download.portal_product_pricelist_page", values)
        else:
            return request.render('website.page_404')

    @http.route("/customer/pricelist", type="http", auth="user", website=True, methods=['POST'])
    def get_customer_pricelist(self, **post):
        partner = request.env.user.partner_id
        if partner.property_product_pricelist and partner.allow_pricelist_download:
            pricelist_file_type = post.get("pricelist_file_type")
            pricelist_product_categ = post.get("pricelist_product_categ")
            values_to_render = {'report_type': 'pdf'}
            if pricelist_product_categ:
                e_com_categ = request.env["product.public.category"].browse(int(pricelist_product_categ))
                e_com_categ_self_child = e_com_categ + e_com_categ.child_id
                pricelist_products = partner.get_pricelist_rules(e_com_categ_self_child.ids)
                values_to_render.update(e_com_categ=e_com_categ)
            else:
                pricelist_products = partner.get_pricelist_rules()
            values_to_render.update(pricelist_products=pricelist_products,
                                    currency_id=partner.property_product_pricelist.currency_id,
                                    current_date=format_date(request.env, fields.Datetime.now(),
                                                             lang_code=get_lang(request.env).code))
            if pricelist_file_type == "pdf":
                report_sudo = request.env.ref('pricelist_portal_download.product_pricelist_action_report').sudo()
                report = report_sudo._render_qweb_pdf([partner.id], data=values_to_render)[0]
                filename = "Product Pricelist - " + fields.Datetime.now().strftime("%Y/%m/%d") + ".pdf"

                content_type = ('Content-Type', 'application/pdf')
                disposition_content = ('Content-Disposition', content_disposition(filename))
                return request.make_response(report, [content_type, disposition_content])
            elif pricelist_file_type == "excel":
                report = self.render_excel_pricelist(values_to_render)
                file_content = base64.b64decode(report or "")

                filename = "Product Pricelist - " + fields.Datetime.now().strftime("%Y/%m/%d") + ".xlsx"

                content_type = ('Content-Type', 'application-/octet-stream')
                disposition_content = ('Content-Disposition', content_disposition(filename))
                return request.make_response(file_content, [content_type, disposition_content])

        else:
            return request.render('website.page_404')

    def render_excel_pricelist(self, values_to_render):
        target_stream = io.BytesIO()
        workbook = xlsxwriter.Workbook(target_stream)
        worksheet = workbook.add_worksheet("Product Pricelist")

        # align_center = workbook.add_format({'valign': 'vcenter', 'align': 'center'})
        head_format = workbook.add_format({'valign': 'vcenter', 'align': 'center', 'bold': True, 'bg_color': 'gray'})
        head_format_center = workbook.add_format(
            {'valign': 'vcenter', 'align': 'center', 'bold': True, 'bg_color': 'yellow'})
        head_format_left = workbook.add_format({'valign': 'vcenter', 'bold': True, })
        format_right = workbook.add_format({'valign': 'vcenter', 'bold': True, 'align': 'right'})
        format_center = workbook.add_format({'valign': 'vcenter', 'bold': False, 'align': 'center'})
        table_row = 5
        for i in range(6):
            worksheet.set_column(0, i, 20)
        if values_to_render.get("pricelist_products"):
            worksheet.merge_range(0, 0, 1, 5, "Product Pricelist", head_format_center)
            worksheet.write(2, 5, "Date: " + values_to_render["current_date"], head_format_left)

            if values_to_render.get("e_com_categ"):
                worksheet.write(2, 0, "Product Category: " + values_to_render["e_com_categ"].name, head_format_left)
            worksheet.set_column('E:F', 30)
            worksheet.set_column('C:C', 40)

            worksheet.write('A5', 'Internal Ref.', head_format)
            worksheet.write('B5', 'Barcode', head_format)
            worksheet.write('C5', 'Product Name', head_format)
            worksheet.write('D5', 'Min. Quantity', head_format)
            worksheet.write('E5', 'Price Duration', head_format)
            worksheet.write('F5', 'Price', head_format)
            # worksheet.write('G5', 'On Hand Qty.', head_format)

            for pricelist_product in values_to_render.get("pricelist_products"):
                worksheet.write(table_row, 0, pricelist_product['product_id'].default_code or "")
                worksheet.write(table_row, 1, pricelist_product['product_id'].barcode or "")
                worksheet.write(table_row, 2,
                                pricelist_product['product_id'].with_context(display_default_code=False).display_name)
                worksheet.write(table_row, 3, pricelist_product['min_qty'] or "-", format_center)
                worksheet.write(table_row, 4, pricelist_product['price_duration'], format_center)
                worksheet.write(table_row, 5, self.format_currency_amount(pricelist_product['price'],
                                                                          values_to_render.get("currency_id")),
                                format_right)
                # if pricelist_product['show_product_stock']:
                #     worksheet.write(table_row, 6, pricelist_product['stock_on_hand'], format_center)
                # else:
                #     if pricelist_product['stock_on_hand'] > 0:
                #         worksheet.write(table_row, 6, "In Stock", format_center)
                #     else:
                #         worksheet.write(table_row, 6, "Out Of Stock", format_center)

                table_row += 1
        else:
            worksheet.merge_range(0, 0, 1, 5, "You do not have any products in the pricelist!", head_format_left)
        workbook.close()
        target_stream.seek(0)
        output = base64.encodebytes(target_stream.read())
        return output

    def format_currency_amount(self, amount, currency_id):
        fmt = "%.{0}f".format(currency_id.decimal_places)
        lang = request.env['ir.qweb.field'].user_lang()

        formatted_amount = lang.format(fmt, currency_id.round(amount),
                                       grouping=True, monetary=True).replace(r' ', u'\N{NO-BREAK SPACE}').replace(r'-',
                                                                                                                  u'-\N{ZERO WIDTH NO-BREAK SPACE}')
        pre = currency_id.position == 'before'
        symbol = u'{symbol}'.format(symbol=currency_id.symbol or '')
        return u'{pre}{0}{post}'.format(formatted_amount, pre=symbol if pre else '', post=symbol if not pre else '')
