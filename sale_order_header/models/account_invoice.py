from odoo import fields, models


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    header_text = fields.Char(string="Header", help="Header or title of the Invoice")
