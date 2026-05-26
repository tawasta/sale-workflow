from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_marking = fields.Char(copy=False)
