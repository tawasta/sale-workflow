from odoo import fields, models
from odoo import Command


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _invoice_sale_orders(self):
        res = super()._invoice_sale_orders()

        for tx in self.filtered(lambda tx: tx.sale_order_ids):
            tx = tx.with_company(tx.company_id)
            for sale_order in tx.sale_order_ids:
                for invoice in sale_order.invoice_ids.ids:
                    if invoice not in tx.invoice_ids.ids:
                        # Link missing invoices to transaction
                        tx.invoice_ids = [Command.link(invoice)]

        return res
