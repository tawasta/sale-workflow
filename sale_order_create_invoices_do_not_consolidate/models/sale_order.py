from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _get_invoice_grouping_keys(self):
        """We prevent consolidating invoices by adding 'invoice_origin' to the
        grouping keys. That way grouping is done per sale order reference, so
        one invoice per sale order. Note that 'id' would not work here."""

        context = self._context

        if context.get("no_consolidate", False):
            return ["company_id", "partner_id", "currency_id", "invoice_origin"]
        else:
            return ["company_id", "partner_id", "currency_id"]
