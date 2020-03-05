from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    use_contract = fields.Boolean("Use contract", default=True)
