from odoo import http
from odoo.http import request

class PaymentControllenedfr(http.Controller):

    @http.route('/collect-payment', type='json', auth='public', methods=['GET', 'POST'],)
    def collect_payment(self, **kwargs):
        website = request.env['website'].get_current_website()
        response_data = website.allow_out_of_stock_order   
        return response_data

        

