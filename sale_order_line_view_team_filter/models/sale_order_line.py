
from odoo import fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    team_id = fields.Many2one(related="order_id.team_id")
