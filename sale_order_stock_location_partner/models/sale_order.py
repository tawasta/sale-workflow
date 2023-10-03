from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        for record in self:
            record.partner_shipping_id.create_stock_location()
        return super(SaleOrder, self).action_confirm()
