from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    auto_confirm_invoice = fields.Boolean(
        string="Auto Confirm Invoices",
        compute="_compute_auto_confirm_invoice",
        store=True,
    )

    @api.depends("order_line.product_id")
    def _compute_auto_confirm_invoice(self):
        for order in self:
            lines = order.order_line.filtered("product_id")
            order.auto_confirm_invoice = bool(lines) and all(
                line.product_id.auto_confirm_sale_invoice for line in lines
            )

    def action_disable_auto_confirm(self):
        self.write({"auto_confirm_invoice": False})

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super()._create_invoices(grouped=grouped, final=final, date=date)

        for invoice in invoices:
            lines = invoice.invoice_line_ids.filtered("product_id")
            auto_confirm_invoice = bool(lines) and all(
                line.product_id.auto_confirm_sale_invoice for line in lines
            )

            if auto_confirm_invoice and invoice.state == "draft":
                invoice.action_post()
                invoice.message_post(
                    body=_(
                        "💡 This invoice was auto-confirmed "
                        "because all products allow auto-confirm."
                    )
                )

        return invoices
