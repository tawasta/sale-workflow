from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            if hasattr(order, "website_id") and order.website_id:
                # Don't unsubscribe e-commerce users,
                # they won't be able to access their SO
                continue
            # We can't prevent the subscription, so we'll just
            # unsubscribe right after the confirmation
            if order.partner_id in order.message_partner_ids:
                order.message_unsubscribe([order.partner_id.id])
        return res
