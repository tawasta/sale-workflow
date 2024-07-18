from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    product_id = fields.Many2one(
        check_company=False,
    )
