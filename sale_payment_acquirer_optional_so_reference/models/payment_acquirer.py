from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    so_reference_type = fields.Selection(
        selection_add=[("null", "Do not create a reference")]
    )
