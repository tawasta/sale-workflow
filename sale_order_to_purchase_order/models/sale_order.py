# -*- coding: utf-8 -*-
from openerp import models, fields, api, _, exceptions


class SaleOrder(models.Model):  

    _inherit = 'sale.order'    
    
    @api.multi
    def copy(self, default=None):
        # When copying a sale order, exclude the purchase order info
        self.ensure_one()
        default = default or {}
        default['purchase_order_ids'] = False
        return super(SaleOrder, self).copy(default)

    purchase_order_ids = fields.One2many('purchase.order', 'sale_order_id', 'Purchase Orders', help='''Purchase Orders created from this Sale Order''') 
