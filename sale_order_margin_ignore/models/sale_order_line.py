# -*- coding: utf-8 -*-

from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.depends('product_id', 'purchase_price', 'product_uom_qty',
                 'price_unit', 'price_subtotal')
    def _product_margin(self):

        super(SaleOrderLine, self)._product_margin()

        for line in self:
            if line.product_id.margin_ignore:
                line.margin = 0
