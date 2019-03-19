# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def action_mark_invoiced(self):
        # Set sale and its lines as invoiced
        self.ensure_one()

        self.invoice_status = "invoiced"

        for line in self.order_line:
            line.invoice_status = "invoiced"
