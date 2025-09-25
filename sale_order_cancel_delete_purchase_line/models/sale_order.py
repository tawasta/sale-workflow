from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_cancel(self):
        res = super().action_cancel()

        purchase_orders = self._get_purchase_orders()

        for po in purchase_orders:
            po.button_cancel()
            po.button_draft()
            for line in po.order_line:
                line.unlink()

        return res
