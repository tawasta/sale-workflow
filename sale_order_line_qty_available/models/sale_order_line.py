from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_qty_available = fields.Float(
        string="Available",
        digits="Product Unit",
        compute="_compute_product_qty_available",
        readonly=True,
    )

    @api.depends("product_uom_qty", "product_uom_id", "product_id")
    def _compute_product_qty_available(self):
        for record in self:
            record.product_qty_available = record.product_id.qty_available
