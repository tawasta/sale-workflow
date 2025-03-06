from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    warranty_clause = fields.Text(string="Warranty Clause")
