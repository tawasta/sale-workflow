from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Tuotteen pitää olla shared product.
    # Laskuttava firma tulee variantilta: product.product.variant_company_id.
    company_id = fields.Many2one(required=False)
