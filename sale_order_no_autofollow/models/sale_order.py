from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            # We can't prevent the subscription, so we'll just
            # unsubscribe right after the confirmation
            if order.partner_id in order.message_partner_ids:
                order.message_unsubscribe([order.partner_id.id])
        return res
