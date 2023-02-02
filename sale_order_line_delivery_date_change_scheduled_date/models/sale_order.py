from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.onchange("commitment_date")
    def _onchange_commitment_date(self):
        for line in self.order_line:
            line.line_delivery_date = self.commitment_date

        return super()._onchange_commitment_date()
