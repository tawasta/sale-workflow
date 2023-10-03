from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    handler = fields.Many2one(
        comodel_name="res.partner",
        string="Handler",
    )
