from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    warehouse_id = fields.Many2one(copy=False)
