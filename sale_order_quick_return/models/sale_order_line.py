from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    stock_moves = fields

    def action_sale_order_line_return(self):
        self.ensure_one()

        if self.product_uom_qty < 0:
            raise UserError(_("You can only return delivered products."))

        # Search a picking to return
        stock_moves = self.env["stock.move"].search(
            [
                ("picking_id", "in", self.order_id.picking_ids.ids),
                ("product_id", "=", self.product_id.id),
                ("state", "=", "done"),
            ],
            order="product_uom_qty",
        )

        if not stock_moves:
            raise UserError(_("This product does not have any deliveries to return."))

        stock_move = stock_moves[0]
        picking = stock_move.picking_id

        return {
            "name": "Picking return",
            "type": "ir.actions.act_window",
            "res_model": "stock.return.picking",
            "view_mode": "form",
            "view_type": "form",
            "target": "new",
            "context": {
                "active_ids": picking.ids,
                "active_id": picking.id,
                "to_refund_so": False,
            },
        }
