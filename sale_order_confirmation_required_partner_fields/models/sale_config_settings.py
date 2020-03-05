from odoo import fields, models


class SaleConfigSettings(models.TransientModel):

    _inherit = "sale.config.settings"

    mandatory_partner_field_ids = fields.Many2many(
        related="company_id.mandatory_partner_field_ids",
        string="Mandatory Partner Fields",
    )
