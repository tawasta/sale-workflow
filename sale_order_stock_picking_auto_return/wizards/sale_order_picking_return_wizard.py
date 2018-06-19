# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrderPickingReturnWizard(models.TransientModel):

    _name = 'sale.order.picking.return.wizard'

    def action_return_picking(self):
        # Sale order cancel with picking return

        sale = self._get_sale_order()

        for picking in sale.picking_ids:

            StockReturnPicking = self.env['stock.return.picking']

            context = dict(
                active_id=picking.id,
                location_id=picking.location_id,
            )
            return_wizard = StockReturnPicking.new()

            return_wizard.with_context(context).force_create_returns(
               location_id=picking.location_id,
            )

        sale.action_cancel()

    def action_cancel(self):
        # Default sale order cancel

        sale = self._get_sale_order()
        sale.action_cancel()

    def _get_sale_order(self):
        self.ensure_one()

        sale_ids = self._context.get('active_ids')

        act_close = {'type': 'ir.actions.act_window_close'}

        if sale_ids is None:
            return act_close

        assert len(sale_ids) == 1, "Only 1 sale ID expected"

        sale = self.env['sale.order'].browse(sale_ids)

        return sale
