from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.depends("product_id", "company_id", "currency_id", "product_uom")
    def _compute_purchase_price(self):
        # If there is no need for UOM or currency conversion,
        # allow skipping the automatic cost price computation
        for line in self:
            line = line.with_company(line.company_id)
            product = line.product_id
            fro_cur = product.cost_currency_id
            to_cur = line.currency_id or line.order_id.currency_id

            uom_match = line.product_uom and line.product_uom == product.uom_id
            cur_match = fro_cur == to_cur

            if uom_match and cur_match and line.purchase_price != 0:
                # Don't update the price
                pass
            else:
                super(SaleOrderLine, line)._compute_purchase_price()
