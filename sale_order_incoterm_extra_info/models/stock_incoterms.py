from odoo import fields, models


class StockIncoterms(models.Model):

    _inherit = "stock.incoterms"

    append_partner_name = fields.Boolean(
        string="Show Customer in Extra Info",
        default=False,
        help=(
            "Adds the customer shipping address to Incoterm Extra Info"
            "field on Sale Order"
        ),
    )
