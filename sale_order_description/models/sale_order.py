from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    description = fields.Text(string="Description", help="Internal notes")
