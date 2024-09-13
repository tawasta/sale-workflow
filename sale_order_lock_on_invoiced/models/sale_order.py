from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        # Create new invoice
        res = super()._create_invoices(grouped=grouped, final=final, date=date)

        # If order state is changed to fully invoiced or upselling, lock it
        # (TimoK: The change has been made because of T68578)
        for order in self:
            if order.invoice_status in ["invoiced", "upselling"]:
                order.action_done()

        return res
