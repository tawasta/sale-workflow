# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    description = fields.Text(
        string='Description',
        help='Internal notes'
    )
