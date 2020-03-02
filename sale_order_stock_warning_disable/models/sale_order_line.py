from odoo import models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    def _onchange_product_id_check_availability(self):
        # Disable the stock level check when selecting a product for SO line
        return {}
