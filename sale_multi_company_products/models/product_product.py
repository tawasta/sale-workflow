from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    invoice_company_id = fields.Many2one(
        "res.company",
        string="Invoicing Company",
        help="Which company receives payment for this product in the "
        "webshop and issues its invoice / uses its payment methods. "
        "Distinct from 'Variant Company' (visibility/access scoping only, "
        "see the product_variant_variant_company module) and from "
        "'Company' (may be blank for products shared between companies). "
        "Empty by default: falls back to the order's own company when "
        "not set (see sale.order._get_split_invoice_companies()).",
    )
