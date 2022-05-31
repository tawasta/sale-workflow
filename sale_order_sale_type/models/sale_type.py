from odoo import fields, models


class SaleType(models.Model):
    _name = 'sale.type'

    name = fields.Char(
        string="Sale Type",
    )

    code = fields.Char(
        string="Sale Type Code",
    )
