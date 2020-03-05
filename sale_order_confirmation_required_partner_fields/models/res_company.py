from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    mandatory_partner_field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        domain=[("model", "=", "res.partner")],
        string="Mandatory Partner Fields",
        help=(
            """The selected fields have to be set for the SO partner
              before order confirmation"""
        ),
    )
