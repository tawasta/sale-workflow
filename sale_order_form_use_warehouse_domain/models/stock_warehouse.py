
from odoo import fields, models


class StockWarehouse(models.Model):

    _inherit = 'stock.warehouse'

    is_usable_warehouse = fields.Boolean(
        string="Is a usable warehouse?",
        copy=False,
        store=True,
        default=True
    )
