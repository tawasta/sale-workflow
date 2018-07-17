# -*- coding: utf-8 -*-
from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
                    stock_move = StockMove.search([
                        ('picking_id', 'in', order.picking_ids.ids),
                        ('product_id', '=', line.product_id.id),
                        ('state', '=', 'done'),
                    ])

                    if stock_move:
                        pick = stock_move.picking_id

                        # Create return picking that will not affect the
                        # delivery amounts

                        default_data = StockReturnPicking.with_context(
                            active_ids=pick.ids,
                            active_id=pick.ids[0]).default_get(
                            ['move_dest_exists', 'original_location_id',
                             'product_return_moves', 'parent_location_id',
                             'location_id'])

                        return_wiz = StockReturnPicking.with_context(
                            active_ids=pick.ids, active_id=pick.ids[0]).create(
                            default_data)

                        return_move = return_wiz.product_return_moves.filtered(
                            lambda r: r.product_id == line.product_id
                        )

                        return_move.quantity = \
                            line.product_uom_qty
                        return_move.to_refund_so = False
                        wiz_response = return_wiz.create_returns()

                        return_pick = StockPicking.browse(
                            wiz_response['res_id']
                        )

                        return_pick.message_post(
                            _('This return was auto-created from a negative'
                              ' sale order line')
                        )

        return res
