from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    weight = fields.Float(
        "Weight", digits=dp.get_precision("Stock Weight"), compute="_compute_weight"
    )

    @api.onchange("product_id", "product_uom", "product_uom_qty")
    def _compute_weight(self):
        for record in self:
            # Negative quantity doesn't have a weight
            uom_qty = record.product_uom_qty if record.product_uom_qty >= 0 else 0
            qty = record.product_uom._compute_quantity(
                uom_qty, record.product_id.uom_id
            )

            weight = qty * record.product_id.weight

            record.weight = weight
