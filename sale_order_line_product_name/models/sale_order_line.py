from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_name = fields.Char(
        related="product_id.product_tmpl_id.name",
    )
