from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    week_of_shipment = fields.Int(string="Week of shipment")
