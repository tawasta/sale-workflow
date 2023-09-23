from odoo import fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    handler = fields.Many2one(
        "res.partner",
        string="Handler",
    )
