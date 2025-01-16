from odoo import _, models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def copy(self, default=None):
        if default is None:
            default = {}

        # Force recalculation with the same logic as in sale and sale_maangement
        # core _compute_require_payment()
        if self.sale_order_template_id:
            default.update(
                {"require_payment": self.sale_order_template_id.require_payment}
            )
        else:
            default.update({"require_payment": self.company_id.portal_confirmation_pay})

        return super().copy(default)
