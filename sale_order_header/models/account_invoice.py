from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    header_text = fields.Char(string="Header", help="Header or title of the Invoice")
