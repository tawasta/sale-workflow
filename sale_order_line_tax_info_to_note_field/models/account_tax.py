from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    sale_order_note = fields.Text(
        string="Note to Sale Order",
        translate=True,
        help="Gets copied to Sale Order notes field, when this tax is used on a Sale "
        "Order line",
    )
