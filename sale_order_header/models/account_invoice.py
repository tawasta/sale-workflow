from odoo import models, fields


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    header_text = fields.Char(
        string="Header",
        help="Header or title of the Invoice"
    )
