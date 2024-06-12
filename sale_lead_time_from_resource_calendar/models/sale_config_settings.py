from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    sale_lead_time_resource_calendar_id = fields.Many2one(
        related="company_id.sale_lead_time_resource_calendar_id",
        readonly=False,
    )
