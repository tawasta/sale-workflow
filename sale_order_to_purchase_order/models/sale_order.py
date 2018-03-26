# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def copy(self, default=None):
        # When copying a sale order, exclude the purchase order info
        self.ensure_one()
        default = default or {}
        default['purchase_order_ids'] = False
        return super(SaleOrder, self).copy(default)

    purchase_order_ids = fields.One2many(
        comodel_name='purchase.order',
        inverse_name='sale_order_id',
        string='Purchase Orders',
        help='Purchase Orders created from this Sale Order'
    )
