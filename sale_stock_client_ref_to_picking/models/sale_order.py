from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            picking_values = {
                "customer_reference": record.client_order_ref,
            }
            record.picking_ids.write(picking_values)

        return res
