from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("partner_id")
    def _compute_partner_shipping_id(self):
        for order in self:
            order.partner_shipping_id = order.partner_id if order.partner_id else False
