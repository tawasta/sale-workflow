# -*- coding: utf-8 -*-
from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_id')
    def _compute_name(self):
        """
        Don't auto-generate description from product/variants.
        Keep whatever is already in `name` (user/manual/custom code).
        """
        # IMPORTANT: do not call super()
        for line in self:
            # Do not overwrite existing name; do nothing.
            # If you want to force empty on new lines too, keep it as-is.
            pass
