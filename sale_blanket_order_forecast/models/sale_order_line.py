from odoo import api
from odoo import fields
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
