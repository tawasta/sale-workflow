from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _get_purchase_ids(self):
        for sale in self:
            sale._get_purchase_orders()
            sale.purchase_order_ids = sale._get_purchase_orders()

    purchase_order_ids = fields.Many2many(
        compute=_get_purchase_ids,
        comodel_name="purchase.order",
        string="Purchase Orders",
    )
