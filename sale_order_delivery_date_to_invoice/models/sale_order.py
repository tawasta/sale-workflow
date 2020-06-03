from odoo import api
from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        # Add delivery date to values
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        date_delivered = False
        if self.effective_date:
            # The "correct" scenario: effective date is set
            date_delivered = self.effective_date
        elif self.commitment_date:
            # Fallback to commitment date
            if self.expected_date and self.expected_date > self.commitment_date:
                # Expected date is after commitment date.
                # Use expected date
                date_delivered = self.expected_date.date()
            else:
                date_delivered = self.commitment_date.date()
        elif self.expected_date:
            # No effective or commitment date. Fallback to expected date
            date_delivered = self.expected_date.date()

        if date_delivered:
            invoice_vals["date_delivered"] = date_delivered.isoformat()

        return invoice_vals
