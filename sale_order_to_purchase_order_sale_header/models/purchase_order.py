# -*- coding: utf-8 -*-
from odoo import models, fields


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    so_header_text = fields.Char(
        related='sale_order_id.header_text',
        string='Sale Order Header'
    )
