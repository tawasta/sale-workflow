from odoo import fields, models


class SaleAdvancePaymentInv(models.TransientModel):

    _inherit = "sale.advance.payment.inv"

    no_consolidate = fields.Boolean(string="Do not consolidate invoices", default=False)

    def create_invoices(self):
        if self.no_consolidate:
            return super(
                SaleAdvancePaymentInv, self.with_context(no_consolidate=True)
            ).create_invoices()
        else:
            return super().create_invoices()
