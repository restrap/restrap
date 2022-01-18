# -*- coding: utf-8 -*-
# from odoo import http


# class Restrap(http.Controller):
#     @http.route('/restrap/restrap', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restrap/restrap/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restrap.listing', {
#             'root': '/restrap/restrap',
#             'objects': http.request.env['restrap.restrap'].search([]),
#         })

#     @http.route('/restrap/restrap/objects/<model("restrap.restrap"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restrap.object', {
#             'object': obj
#         })
