from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    auto_confirm_invoice = fields.Boolean(
        string="Auto Confirm Invoices",
        compute="_compute_auto_confirm_invoice",
    )

    @api.depends("order_line.product_id")
    def _compute_auto_confirm_invoice(self):
        for order in self:
            lines = order.order_line.filtered("product_id")
            order.auto_confirm_invoice = bool(lines) and all(
                line.product_id.auto_confirm_sale_invoice for line in lines
            )
