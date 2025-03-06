from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_reference = fields.Char(
        related="product_id.code",
    )
