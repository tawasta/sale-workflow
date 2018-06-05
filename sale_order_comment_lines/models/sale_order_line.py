# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    def _get_to_invoice_qty(self):
        super(SaleOrderLine, self)

        # Force invoicing lines that have products with force_invoicing
        for line in self:
            if line.product_id.force_invoicing:
                line.qty_to_invoice = 1
