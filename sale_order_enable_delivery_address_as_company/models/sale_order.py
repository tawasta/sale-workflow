from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("partner_id")
    def _compute_partner_shipping_id(self):
        for order in self:
            partner_shipping = (
                order.partner_id.address_get(["delivery"])["delivery"]
                if order.partner_id
                else False
            )

            if partner_shipping:
                order.partner_shipping_id = partner_shipping
            else:
                # Search all delivery addresses, including company type ones
                shipping_address_ids = order.partner_id.address_ids.filtered(
                    lambda x: x.type == "delivery"
                )

                # Set delivery address as first record from the list
                order.partner_shipping_id = (
                    shipping_address_ids and shipping_address_ids[0] or False
                )
