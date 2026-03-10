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
        for line in self:
            # If empty, set a dash to avoid issues with the name field
            # being entirely empty.
            #
            # If not empty, intentionally do nothing to prevent Odoo from
            # overwriting the existing (manually written) description.
            if not line.name:
                line.name = "-"
