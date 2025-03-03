from odoo import fields, models


class SaleType(models.Model):
    _name = "sale.type"
    _description = "Sale Type"

    name = fields.Char(
        string="Sale Type",
    )

    code = fields.Char(
        string="Sale Type Code",
    )
