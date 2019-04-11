# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def action_mark_invoiced(self):
        # Set sale and its lines as invoiced
        self.ensure_one()

        # Lock the SO
        self.action_done()

        # Force SO state
        self.invoice_status = "invoiced"

        # Force state for SO lines
        for line in self.order_line:
            line.invoice_status = "invoiced"
