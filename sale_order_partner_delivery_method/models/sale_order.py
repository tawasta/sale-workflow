from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.onchange("partner_id")
    def onchange_partner_id_carrier_id(self):
        if self.partner_id:
            self.carrier_id = self.partner_id.property_delivery_carrier_id.filtered(
                "active"
            )
