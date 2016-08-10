# -*- coding: utf-8 -*-
from openerp import http

# class Odoo-s3(http.Controller):
#     @http.route('/odoo-s3/odoo-s3/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-s3/odoo-s3/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-s3.listing', {
#             'root': '/odoo-s3/odoo-s3',
#             'objects': http.request.env['odoo-s3.odoo-s3'].search([]),
#         })

#     @http.route('/odoo-s3/odoo-s3/objects/<model("odoo-s3.odoo-s3"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-s3.object', {
#             'object': obj
#         })