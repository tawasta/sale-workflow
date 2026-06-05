from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    order_line_ref = fields.Char(copy=False)
