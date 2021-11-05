
from odoo import fields, models


class PaymentAcquirer(models.Model):

    _inherit = 'payment.acquirer'

    so_reference_type = fields.Selection(
        selection_add=[('null', 'None')])
