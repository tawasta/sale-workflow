# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('state', 'product_uom_qty', 'qty_delivered', 'qty_to_invoice',
                 'qty_invoiced')
    def _compute_invoice_status(self):
        super(SaleOrderLine, self)._compute_invoice_status()

        for line in self:

            if line.invoice_status == 'upselling' and line.product_uom_qty < 0:
                # If a deliverable product has a negative saldo
                # but has been invoiced, mark it as invoiced
                precision = self.env['decimal.precision'].precision_get(
                    'Product Unit of Measure'
                )

                # Re-check if line is invoiced
                # Normally "not fully delivered" will override this
                if float_compare(line.qty_invoiced, line.product_uom_qty,
                                 precision_digits=precision) >= 0:
                    line.invoice_status = 'invoiced'
