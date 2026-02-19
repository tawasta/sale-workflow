from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id")
    def _compute_name(self):
        """
        Do not auto-generate the description from the product or variants.
        Keep whatever is already stored in `name`.
        """
        # IMPORTANT: do not call super()
        for _ in self:
            # Intentionally do nothing to prevent Odoo from
            # overwriting the existing description.
            pass
