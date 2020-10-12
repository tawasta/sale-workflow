from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    mandatory_partner_field_ids = fields.Many2many(
        string="Mandatory Partner Fields",
        related="company_id.mandatory_partner_field_ids",
        readonly=False,
    )
