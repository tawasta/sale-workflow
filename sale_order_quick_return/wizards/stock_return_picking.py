from odoo import models


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def create_returns(self):
        res = super(StockReturnPicking, self).create_returns()

        picking_id = res.get("res_id")
        picking = self.env["stock.picking"].browse([picking_id])
        sale_id = picking.sale_id

        for move in picking.move_lines:
            # Create a negative line for sale order
            sale_order_line = sale_id.order_line.filtered(
                lambda r: move.product_id == r.product_id
            )[0]

            sale_order_line.copy(
                {"product_uom_qty": move.product_uom_qty * -1, "order_id": sale_id.id}
            )

        return res
