# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    invoice_state = fields.Selection(
        string='Invoice state',
        selection=[
            ('draft', 'Draft'),
            ('proforma', 'Pro-forma'),
            ('proforma2', 'Pro-forma'),
            ('open', 'Open'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ],
        compute='_compute_invoice_state',
    )

    def _compute_invoice_state(self):
        for record in self:
            invoice_state = False
            for invoice in record.invoice_ids:
                # Prefer open invoices
                if not invoice_state or \
                        invoice.state not in ['paid', 'cancel']:
                    invoice_state = invoice.state

            record.invoice_state = invoice_state
