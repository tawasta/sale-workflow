from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()
        if self.description:
            invoice_vals["description"] = self.description

        return invoice_vals
