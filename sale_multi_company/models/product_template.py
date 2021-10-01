from odoo import api
from odoo import fields
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    company_id = fields.Many2one(
        required=True,
    )
