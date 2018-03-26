# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def copy(self, default=None):
        # When copying a purchase order, exclude the Sale Order info
        self.ensure_one()
        default = default or {}
        default['sale_order_id'] = False
        return super(PurchaseOrder, self).copy(default)

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        help='The Sale Order this Purchase originated from'
    )

    so_client_order_ref = fields.Char(
        related='sale_order_id.client_order_ref',
        string='Sale Order Customer Reference'
    )
