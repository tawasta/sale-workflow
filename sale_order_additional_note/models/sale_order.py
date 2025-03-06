from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    additional_note = fields.Html(string="Additional Notes", copy=False)
