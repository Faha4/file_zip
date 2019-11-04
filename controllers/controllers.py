# -*- coding: utf-8 -*-
from odoo import http

# class PrimeExep(http.Controller):
#     @http.route('/prime_exep/prime_exep/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/prime_exep/prime_exep/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('prime_exep.listing', {
#             'root': '/prime_exep/prime_exep',
#             'objects': http.request.env['prime_exep.prime_exep'].search([]),
#         })

#     @http.route('/prime_exep/prime_exep/objects/<model("prime_exep.prime_exep"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('prime_exep.object', {
#             'object': obj
#         })