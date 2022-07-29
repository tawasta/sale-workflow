from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    client_order_ref = fields.Char(
        copy=True,
    )
