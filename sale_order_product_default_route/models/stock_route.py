
from odoo import fields, models


class StockLocationRoute(models.Model):

    _inherit = "stock.location.route"

    use_on_sale_line = fields.Boolean(string="Use this on Sale Order line", copy=False)
