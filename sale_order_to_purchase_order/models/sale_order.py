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

    @api.multi
    def _compute_purchase_status(self):
        ''' Set the status based on the individual PO states
        - No Purchases: no POs linked to the SO
        - Purchase Exception: any POs are in Cancel state
        - Fully Confirmed: all POs are in Purchase Order or Done states
        - To Confirm: some POs are still in RFQ/Sent/To Approve states '''

        for sale in self:
            if not sale.purchase_order_ids:
                sale.purchase_status = 'none'
            else:
                if all([po.state in ['purchase', 'done']
                       for po in sale.purchase_order_ids]):
                    sale.purchase_status = 'done'
                elif any([po.state == 'cancel'
                         for po in sale.purchase_order_ids]):
                    sale.purchase_status = 'exception'
                else:
                    sale.purchase_status = 'open'

    purchase_order_ids = fields.One2many(
        comodel_name='purchase.order',
        inverse_name='sale_order_id',
        string='Purchase Orders',
        help='Purchase Orders created from this Sale Order'
    )

    purchase_status = fields.Selection(
        selection=[('none', 'No Purchases'),
                   ('open', 'To Confirm'),
                   ('done', 'Fully Confirmed'),
                   ('exception', 'Purchase Exception')],
        compute='_compute_purchase_status',
        string='Purchase Status')
