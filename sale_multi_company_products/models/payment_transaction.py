from odoo import Command, models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _invoice_sale_orders(self):
        res = super()._invoice_sale_orders()

        for tx in self.sudo().filtered(lambda tx: tx.sale_order_ids):
            invoices = tx.sale_order_ids.invoice_ids.filtered(
                lambda move: move.move_type == "out_invoice"
                and move.state != "cancel"
            )

            missing = invoices - tx.invoice_ids
            if missing:
                tx.write({
                    "invoice_ids": [Command.link(invoice.id) for invoice in missing]
                })

        return res