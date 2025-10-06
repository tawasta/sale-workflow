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

            # Search all delivery addresses, including company type ones
            shipping_address_ids = order.partner_id.address_ids.filtered(
                lambda x: x.type == "delivery"
            )

            # Get first delivery address record from the list
            shipping_address_id = (
                shipping_address_ids and shipping_address_ids[0] or False
            )

            delivery_addr_not_customer = (
                shipping_address_id
                and shipping_address_id.id != order.partner_id.id
                or False
            )

            # This might look unnecessarily complicated, but these checks
            # are used for better compatibility with other modules. Because
            # perhaps address_get() -method has been modified.
            if (
                partner_shipping
                and order.partner_id
                and partner_shipping == order.partner_id.id
                and delivery_addr_not_customer
            ):
                order.partner_shipping_id = shipping_address_id
            else:
                order.partner_shipping_id = partner_shipping
