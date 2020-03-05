from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.multi
    @api.onchange("product_id")
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()

        # Override description generation
        product = self.product_id.with_context(lang=self.order_id.partner_id.lang)

        if product and product.description_sale:
            self.name = product.description_sale
        elif product.name:
            self.name = product.name

        return res
