from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.model
    def create(self, values):
        res = super().create(values)
        for sale in res:
            sale.order_line._compute_amount()
        return res

    def write(self, values):
        res = super().write(values)
        if "order_line" in values:
            for sale in self:
                sale.order_line._compute_amount()
        return res
