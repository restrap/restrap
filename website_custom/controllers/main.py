from odoo import http
from odoo.http import request
import json
import re
class PaymentControllenedfr(http.Controller):

    @http.route('/collect-payment', type='json', auth='public', methods=['GET', 'POST'],)
    def collect_payment(self, **kwargs):
        data = json.loads(http.request.httprequest.data.decode('utf-8'))
        current_url = data.get('current_url')
        website = request.env['website'].get_current_website()
        response_data = website.allow_out_of_stock_order
        last_order = request.env['sale.order'].search([
            ('website_id', '=', website.id),
            ('state', 'in', ['draft'])  # Optional: filter by order state
        ], limit=1, order='create_date desc')
        match = re.search(r'/shop/([^/-]+)-(\d+)', current_url)
        qty = 0
        qty2 = 0
        if match:
            product_name = match.group(1)  # Extracted product name
            product_id = match.group(2)     # Extracted product ID
            product = request.env['product.product'].search([('name', '=', product_name)], limit=1)
            stock2 = request.env['report.stock.quantity'].search([('product_id', '=', product.id)], limit=1)
            qty = (product.qty_available + product.incoming_qty) -  product.outgoing_qty
            stock1 = request.env['stock.quant'].search([('product_id', '=', product.id)])
            for stock in stock1:
                if website.warehouse_id.view_location_id == stock.location_id.location_id:
                    qty2 = stock.inventory_quantity_auto_apply - stock.reserved_quantity
        else:
            product_name = None
            product_id = None
        
        if qty2 <= 0 and response_data != True:
            return False
        else:
            return True 

        

