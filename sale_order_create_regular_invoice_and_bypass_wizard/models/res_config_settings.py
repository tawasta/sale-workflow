from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    hide_standard_create_invoice_button = fields.Boolean(
        related="company_id.hide_standard_create_invoice_button",
        readonly=False,
        string="Hide standard 'Create Invoice' button",
        help="If enabled, the standard Odoo 'Create Invoice' button "
        "(which opens the down-payment / regular invoice wizard) "
        "is hidden from the sale order form. Only the "
        "'Create Regular Invoice' button remains.",
    )
