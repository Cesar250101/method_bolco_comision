# -*- coding: utf-8 -*-
from odoo import http

# class MethodBolcoComision(http.Controller):
#     @http.route('/method_bolco_comision/method_bolco_comision/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_bolco_comision/method_bolco_comision/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_bolco_comision.listing', {
#             'root': '/method_bolco_comision/method_bolco_comision',
#             'objects': http.request.env['method_bolco_comision.method_bolco_comision'].search([]),
#         })

#     @http.route('/method_bolco_comision/method_bolco_comision/objects/<model("method_bolco_comision.method_bolco_comision"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_bolco_comision.object', {
#             'object': obj
#         })