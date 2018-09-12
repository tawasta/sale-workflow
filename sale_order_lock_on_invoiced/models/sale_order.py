# -*- coding: utf-8 -*-
from odoo import models, api, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def action_invoice_create(self, grouped=False, final=False):
        # Create new invoice
        res = super(SaleOrder, self).action_invoice_create(
            grouped=grouped,
            final=final,
        )

        # If order state is changed to fully invoiced, lock it
        for order in self:
            if order.invoice_status == 'invoiced':
                order.action_done()

        return res