from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _create_invoices(self, grouped=False, final=False, date=None):
        # Create new invoice
        res = super()._create_invoices(grouped=grouped, final=final, date=date)

        # If order state is changed to fully invoiced, lock it
        for order in self:
            if order.invoice_status == "invoiced":
                order.action_done()

        return res
