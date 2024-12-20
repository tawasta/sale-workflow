from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def write(self, values):
        res = super().write(values)

        product_id = values.get("product_id", False)
        product = self.env["product.product"].browse(product_id)
        warranty_clause = product and product.warranty_clause or False

        if warranty_clause:
            if self.order_id.warranty:
                self.order_id.warranty += "{}{}".format("\n", warranty_clause)
            else:
                self.order_id.warranty += "{}".format(warranty_clause)

        return res

    @api.onchange("product_id")
    def onchange_product_warranty(self):
        if self.order_id.warranty and self._origin.product_id.warranty_clause:
            product = self._origin.product_id

            warranty = self._origin.order_id.warranty.split("\n")
            words_to_remove = product.warranty_clause.split("\n")

            warranty = [
                line
                for line in warranty
                if not any(word in line for word in words_to_remove)
            ]

            warranty = "\n".join(warranty)
            self._origin.order_id.warranty = warranty
