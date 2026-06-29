from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    parent_company_id = fields.Many2one(
        comodel_name="res.company",
        related="parent_id.company_id",
        readonly=True,
    )