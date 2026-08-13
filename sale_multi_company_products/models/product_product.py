from odoo import fields, models
from odoo.osv import expression


def _check_company_domain_with_invoice_company(self, companies):
    """Like models.check_company_domain_parent_of, but also treats a
    product as compatible with a company when its own invoice_company_id
    explicitly says so.

    Without this, Odoo's own check_company constraint on
    account.move.line.product_id (product.product's default
    _check_company_domain only allows a blank company_id or a parent
    company) would reject a split invoice as soon as a product's
    invoice_company_id differs from its own company_id - which is
    exactly the case this field exists for.
    """
    domain = models.check_company_domain_parent_of(self, companies)
    if isinstance(companies, str):
        invoice_domain = [("invoice_company_id", "=", companies)]
    else:
        invoice_domain = [
            ("invoice_company_id", "in", models.to_company_ids(companies))
        ]
    return expression.OR([domain, invoice_domain])


class ProductProduct(models.Model):
    _inherit = "product.product"

    _check_company_domain = _check_company_domain_with_invoice_company

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
