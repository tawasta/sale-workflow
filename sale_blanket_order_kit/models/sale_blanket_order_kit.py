from odoo import fields, models


class SaleBlanketOrderKit(models.Model):
    _name = "sale.blanket.order.kit"

    order_id = fields.Many2one("sale.blanket.order", required=True, ondelete="cascade")

    kit_id = fields.Many2one(
        comodel_name="mrp.bom",
        name="Kit",
        domain=[("type", "=", "phantom")],
        required=True,
    )

    original_uom_qty = fields.Float(
        "Original quantity",
        required=True,
        default=1,
        digits="Product Unit of Measure",
    )
