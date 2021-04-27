from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.onchange("warehouse_id")
    def _onchange_warehouse_id(self):
        # Disable changing the company
        pass
