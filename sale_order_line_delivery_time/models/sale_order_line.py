from odoo import fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    line_delivery_time = fields.Char(string="Delivery Time")
