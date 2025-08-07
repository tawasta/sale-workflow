from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sale_default_payment_term = fields.Many2one(
        comodel_name="account.payment.term",
        string="Default Payment term",
    )
