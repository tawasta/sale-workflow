from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("expected_date")
    def _onchange_commitment_date(self):
        self.commitment_date = self.expected_date
