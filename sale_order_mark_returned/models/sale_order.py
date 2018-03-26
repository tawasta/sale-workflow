# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    returned = fields.Boolean(
        string='Returned',
        help='Products have been shipped but then returned by the customer.'
    )
