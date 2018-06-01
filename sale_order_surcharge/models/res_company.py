# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    surcharge_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Sale Order Surcharge Product',
        help='''Product to use as a surcharge for Sale Orders'''
    )

    surcharge_percentage = fields.Float(
        string='Surcharge Percentage',
        digits=(6, 2),
        help=('''Percentage of the Sale Order untaxed total to be calculated
              as the surcharge price''')
    )
