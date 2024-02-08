import logging

from odoo import _, exceptions, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):

        # Don't enforce the check on autoconfirmed website sales

        for sale in self:

            # Ignore orders autoconfirmed from website
            from_website = hasattr(sale, "website_id") and sale.website_id

            if not from_website and not sale.client_order_ref:
                msg = _("Please fill in the customer reference.")
                raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
