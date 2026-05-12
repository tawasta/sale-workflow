from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    hide_standard_create_invoice_button = fields.Boolean(
        related="company_id.hide_standard_create_invoice_button",
    )

    def action_create_regular_invoice(self):
        """Create a regular invoice directly for this SO, bypassing the
        standard 'sale.advance.payment.inv' wizard.

        Mirrors what the wizard does when the user picks the
        'Regular invoice' option. Finally open the resulting invoice.
        """
        self.ensure_one()

        if self.invoice_status != "to invoice":
            raise UserError(_("There is nothing to invoice on this sale order."))

        moves = self._create_invoices(final=True)

        return self.action_view_invoice(invoices=moves)
