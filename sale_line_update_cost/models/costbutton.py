# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CostButton(models.Model):

    _inherit = 'sale.order.line'

    new_cost = fields.Float(
        string="Actual Cost",
        compute="_compute_update_cost",
        help="Shows the current, actual cost behind the product."
        )

    @api.multi
    def _compute_update_cost(self):

        for record in self:
            product = record.product_id.with_context(
                lang=record.order_id.partner_id.lang,
                partner=record.order_id.partner_id.id,
                quantity=record.product_uom_qty,
                date=record.order_id.date_order,
                pricelist=record.order_id.pricelist_id.id,
                uom=record.product_uom.id
            )

            res = record._get_purchase_price(
                record.order_id.pricelist_id,
                product, record.product_uom, record.order_id.date_order
            )

            record.new_cost = res['purchase_price']

    @api.multi
    def button_cost(self):

        for record in self:

            record.write({'purchase_price': record.new_cost})
