from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        # "Disable" delivery address onchange

        values = dict(
            partner_shipping_id=self.partner_shipping_id,
        )

        super(SaleOrder, self).onchange_partner_id()

        # Do not override when dealing with a website order, to avoid interfering
        # with unregistered users' orders' shipping addresses during checkout
        if not self.env.context.get("website_id"):
            self.update(values)
