from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    auto_confirm_sale_invoice = fields.Boolean(
        string="Invoice Auto Confirm",
        help="If checked, sale invoices containing only products with this flag will be auto-confirmed.",
        default=False,
    )
