from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    hide_standard_create_invoice_button = fields.Boolean(
        string="Hide standard 'Create Invoice' button on sale orders",
        default=False,
    )
