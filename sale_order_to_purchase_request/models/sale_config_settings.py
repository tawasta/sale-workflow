# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleConfigSettings(models.TransientModel):

    _inherit = 'sale.config.settings'

    purchase_request_from_sale_buy = fields.Boolean(
        related='company_id.purchase_request_from_sale_buy',
        help='''Sale confirmation triggers the creation of a Purchase Request
                for those products that are buyable and are missing stock ''')

    purchase_request_from_sale_mrp = fields.Boolean(
        related='company_id.purchase_request_from_sale_mrp',
        string='Purchase Requests from manufacturables',
        help='''Sale confirmation triggers the creation of a Purchase Request
                for those products that are a part of sold items' BOMs
                and are missing stock. ''')

    purchase_request_location_rule = fields.Selection(
        related='company_id.purchase_request_location_rule',
        string='Locations to Check')

    purchase_request_location_ids = fields.Many2many(
        related='company_id.purchase_request_location_ids',
        string='Custom locations')
