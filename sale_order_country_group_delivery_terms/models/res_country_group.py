from odoo import fields, models


class CountryGroup(models.Model):

    _inherit = "res.country.group"
    _order = "sequence, name"

    sequence = fields.Integer()
    skip_delivery_terms = fields.Boolean(string="Skip Delivery terms")
    delivery_terms = fields.Char(string="Delivery Terms")
