from odoo import fields, models


class CountryGroup(models.Model):

    _inherit = "res.country.group"
    _order = "sequence, name"

    sequence = fields.Integer()

    delivery_terms = fields.Char(string="Delivery Terms")
