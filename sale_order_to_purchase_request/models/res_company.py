# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    purchase_request_from_sale_buy = fields.Boolean(
        string='Purchase Requests from buyables',
        help='''Sale confirmation triggers the creation of a Purchase Request
                for those products that are buyable and are missing stock ''')

    purchase_request_from_sale_mrp = fields.Boolean(
        string='Purchase Requests from manufacturables',
        help='''Sale confirmation triggers the creation of a Purchase Request
                for those products that are a part of sold items' BOMs
                and are missing stock. ''')

    purchase_request_location_rule = fields.Selection(
        selection=[('project_and_custom',
                    ('Project Default Location and a list '
                     'of custom locations'))],
        string='Locations to Check',
        help=('Purchase Request will be created if the combined available '
              'stock in these locations is not enough.'))

    purchase_request_location_ids = fields.Many2many(
        comodel_name='stock.location',
        string='Custom locations',
        domain=[('usage', '=', 'internal')],
        help=('List of custom locations to use when checking'
              'available stock'))
