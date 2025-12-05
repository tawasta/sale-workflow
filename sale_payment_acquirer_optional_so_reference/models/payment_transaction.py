from odoo import models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _compute_sale_order_reference(self, order):
        reference = super()._compute_sale_order_reference(order)

        if self.provider_id.so_reference_type == "null":
            return ""
        else:
            return reference
