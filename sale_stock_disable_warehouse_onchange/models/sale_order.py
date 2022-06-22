from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order"

    @api.onchange("warehouse_id")
    def _onchange_warehouse_id(self):
        # Disable company changing on warehouse change
        pass
