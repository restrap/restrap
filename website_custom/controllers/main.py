from odoo import http
from odoo.http import request
import json
import re
class PaymentControllenedfr(http.Controller):

    @http.route('/collect-payment', type='json', auth='public', methods=['GET', 'POST'],)
    def collect_payment(self, **kwargs):
        data = json.loads(http.request.httprequest.data.decode('utf-8'))
        current_url = data.get('current_url')
        main_product = (data.get('product_id_variant_ids'))
        main_product_tmpl = (data.get('product_id'))
        product_id_variant = data.get('product_id_variant')
        website = request.env['website'].get_current_website()
        response_data = website.allow_out_of_stock_order
        qty = 0
        qty2 = 0
        
        if product_id_variant:
            product = request.env['product.product'].search([('id', '=', product_id_variant)])
            stock1 = request.env['stock.quant'].search([('product_id', '=', product.id)])
            for stock in stock1:
                if website.warehouse_id.view_location_id == stock.location_id.location_id:
                    qty2 = stock.inventory_quantity_auto_apply - stock.reserved_quantity
        if main_product:
            product_s = request.env['product.template.attribute.value'].search([('id', '=', main_product)])
            stock2 = request.env['product.product'].search([('product_template_variant_value_ids', '=', product_s.id)])
            stock3 = request.env['stock.quant'].search([('product_id', '=', stock2.id)])
            qty2 = stock2.free_qty
            #for stock34 in stock3:
                #if website.warehouse_id.view_location_id == stock34.location_id.location_id:
                    #print("product_free_qtytttttttttttttttt",stock2.free_qty)
                    #qty2 = stock2.free_qty
                    #qty2 = stock34.inventory_quantity_auto_apply - stock34.reserved_quantity
                    #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&777",stock34.inventory_quantity_auto_apply - stock34.reserved_quantity)
                

        if qty2 <= 0 and response_data != True:
            return False
        else:
            return True 

        

