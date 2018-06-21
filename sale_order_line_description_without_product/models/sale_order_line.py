# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()

        # Override description generation
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
        )

        if product:
            name = product.name_get()[0][1]

            if product.description_sale:
                name = product.description_sale

            self.name = name

        return res
