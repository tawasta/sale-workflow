from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    company_id = fields.Many2one(
        required=True,
    )
