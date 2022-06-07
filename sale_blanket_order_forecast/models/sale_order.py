from odoo import fields
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_forecast = fields.Boolean(default=False)
