from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    customer_order_date = fields.Date(string="Customer order date")
