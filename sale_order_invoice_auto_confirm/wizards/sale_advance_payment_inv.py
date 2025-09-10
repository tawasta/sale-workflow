from odoo import models, _


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        res = super().create_invoices()

        if isinstance(res, dict) and res.get("res_id"):
            invoices = self.env["account.move"].browse(res["res_id"])
        elif isinstance(res, dict) and res.get("domain"):
            invoices = self.env["account.move"].search(res["domain"])
        else:
            invoices = self.env["account.move"].browse()

        for invoice in invoices:
            lines = invoice.invoice_line_ids.filtered("product_id")
            auto_confirm_invoice = bool(lines) and all(
                line.product_id.auto_confirm_sale_invoice for line in lines
            )

            if auto_confirm_invoice:
                invoice.action_post()
                invoice.message_post(
                    body=_(
                        "💡 This invoice was auto-confirmed because all products allow auto-confirm."
                    )
                )
        return res
