from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    check_qty_available = fields.Boolean(
        string="Check qty available",
        help="Do we need to check the availability of this line",
        compute="_compute_product_qty_check_available",
        readonly=1,
    )

    product_qty_available = fields.Float(
        string="Available",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_product_qty_available",
        readonly=1,
    )

    @api.onchange("product_id")
    @api.depends("product_id")
    def _compute_product_qty_check_available(self):
        for record in self:
            order_open = record.state in ("draft", "sent")
            product_stockable = record.product_id.type == "product"

            record.check_qty_available = order_open and product_stockable

    @api.onchange("product_uom_qty", "product_uom", "product_id")
    @api.depends("product_uom_qty", "product_uom", "product_id")
    def _compute_product_qty_available(self):
        for record in self:
            record.product_qty_available = record.product_id.qty_available
