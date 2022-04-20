from odoo import models
from odoo import _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()

        if self.customer_contact_id:
            narration = _("Customer contact: {}".format(self.customer_contact_id.name))
            if invoice_vals.get("narration"):
                narration = f"{invoice_vals['narration']}\n{narration}"
            invoice_vals["narration"] = narration

        return invoice_vals
