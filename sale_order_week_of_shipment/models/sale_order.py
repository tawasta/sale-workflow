from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    week_of_shipment = fields.Integer(string="Week of shipment", readonly=False)
