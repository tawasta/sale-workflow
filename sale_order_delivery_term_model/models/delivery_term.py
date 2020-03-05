from odoo import fields, models


class DeliveryTerm(models.Model):

    _name = 'delivery.term'

    name = fields.Char(
        string='Delivery term',
    )
