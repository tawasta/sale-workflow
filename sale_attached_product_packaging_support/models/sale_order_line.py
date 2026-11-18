from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_attached_line_uom(self, product):
        """Return the unit for an attached product's line:
        - the main line's unit when the product allows it (its own unit or
        one of its packagings),
        - otherwise the product's own unit."""
        self.ensure_one()
        if self.product_uom_id in product.product_tmpl_id._get_available_uoms():
            return self.product_uom_id
        return product.uom_id
