from odoo import models


class SaleOrderPickingReturnWizard(models.TransientModel):

    _name = "sale.order.picking.return.wizard"

    def action_return_picking(self):
        # Sale order cancel with picking return

        sale_order = self._get_sale_order()

        StockReturnPicking = self.env["stock.return.picking"]
        StockMove = self.env["stock.move"]

        for line in sale_order.order_line:
            # Search a move line to return
            stock_moves = StockMove.search(
                [
                    ("picking_id", "in", sale_order.picking_ids.ids),
                    ("product_id", "=", line.product_id.id),
                    ("state", "=", "done"),
                ]
            )

            for stock_move in stock_moves:
                pick = stock_move.picking_id

                default_data = StockReturnPicking.with_context(
                    active_ids=pick.ids, active_id=pick.ids[0]
                ).default_get(
                    [
                        "move_dest_exists",
                        "original_location_id",
                        "parent_location_id",
                        "location_id",
                    ]
                )

                default_data["product_return_moves"] = [
                    (
                        0,
                        0,
                        dict(
                            product_id=stock_move.product_id.id,
                            move_id=stock_move.id,
                            quantity=line.product_uom_qty,
                        ),
                    )
                ]

                return_wiz = StockReturnPicking.with_context(
                    active_ids=pick.ids, active_id=pick.ids[0]
                ).create(default_data)

                return_wiz.product_return_moves.to_refund_so = False

                res = return_wiz.create_returns()

                # Validate picking
                return_pick = self.env["stock.picking"].browse(res["res_id"])
                return_pick.force_assign()
                return_pick.pack_operation_product_ids.write(
                    {"qty_done": line.product_uom_qty}
                )
                return_pick.do_new_transfer()

        sale_order.action_cancel()

    def action_cancel(self):
        # Default sale order cancel

        sale_order = self._get_sale_order()
        sale_order.action_cancel()

    def _get_sale_order(self):
        self.ensure_one()

        sale_ids = self._context.get("active_ids")

        act_close = {"type": "ir.actions.act_window_close"}

        if sale_ids is None:
            return act_close

        assert len(sale_ids) == 1, "Only 1 sale ID expected"

        sale = self.env["sale.order"].browse(sale_ids)

        return sale
