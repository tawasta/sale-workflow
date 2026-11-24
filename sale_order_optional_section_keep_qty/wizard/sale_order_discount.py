from odoo import models


class SaleOrderDiscount(models.TransientModel):
    _inherit = "sale.order.discount"

    def _get_discountable_order_lines(self):
        return (
            super()._get_discountable_order_lines()
            - self.sale_order_id._get_optional_lines()
        )
