from odoo import fields, models


class DeliveryCarrier(models.Model):

    _inherit = 'delivery.carrier'

    min_weight = fields.Float(string="Minimum weight")
    max_weight = fields.Float(string="Maximum weight")
