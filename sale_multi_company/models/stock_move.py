from odoo import api
from odoo import fields
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    product_id = fields.Many2one(
        check_company=False,
    )
