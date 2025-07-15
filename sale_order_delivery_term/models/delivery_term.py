from odoo import fields, models


class DeliveryTerm(models.Model):
    _name = "delivery.term"
    _description = "Delivery Term"

    name = fields.Char(
        string="Delivery term",
    )
