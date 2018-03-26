# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    direct_sale = fields.Boolean(
        string='Direct Sale'
    )
