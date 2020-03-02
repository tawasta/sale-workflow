from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    """
    # This would make the returns on creating an invoice
    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create(
            grouped=grouped,
            final=final,
        )

        StockPicking = self.env['stock.picking']
        StockReturnPicking = self.env['stock.return.picking']
        StockMove = self.env['stock.move']

        for order in self:
            for line in order.order_line:
                if line.product_uom_qty < 0:
                    # Search a move line to return
                    stock_moves = StockMove.search([
                        ('picking_id', 'in', order.picking_ids.ids),
                        ('product_id', '=', line.product_id.id),
                        ('state', '=', 'done'),
                    ])

                    returned_qty = 0
                    to_return_qty = abs(line.product_uom_qty)

                    for stock_move in stock_moves:
                        if returned_qty == to_return_qty:
                            # Everything is returned. Nothing to do
                            continue

                        pick = stock_move.picking_id

                        # Check if we can return all products
                        move_return_qty = to_return_qty

                        if stock_move.product_uom_qty < move_return_qty:
                            move_return_qty = stock_move.product_uom_qty

                        # Create return picking that will not affect the
                        # delivery amounts

                        default_data = StockReturnPicking.with_context(
                            active_ids=pick.ids,
                            active_id=pick.ids[0]).default_get(
                            ['move_dest_exists', 'original_location_id',
                             'parent_location_id', 'location_id'])

                        default_data['product_return_moves'] = [(0, 0, dict(
                            product_id=stock_move.product_id.id,
                            move_id=stock_move.id,
                            quantity=move_return_qty,
                        ))]

                        return_wiz = StockReturnPicking.with_context(
                            active_ids=pick.ids, active_id=pick.ids[0]).create(
                            default_data
                        )

                        return_wiz.product_return_moves.to_refund_so = False

                        wiz_response = return_wiz.create_returns()

                        returned_qty += move_return_qty

                        return_pick = StockPicking.browse(
                            wiz_response['res_id']
                        )

                        return_pick.message_post(
                            _('This return was auto-created when invoicing a '
                              'sale with refundable products (%s)'
                              % order.name)
                        )

        return res
        """
