from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    warranty = fields.Text(related="sale_id.warranty")
