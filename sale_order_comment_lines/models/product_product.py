# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    force_invoicing=fields.Boolean(
        string='Force invoicing',
        help='This product can be invoiced without quantity.'
             '\n'
             'Can be used for e.g. line comments',
        default=False,
    )
