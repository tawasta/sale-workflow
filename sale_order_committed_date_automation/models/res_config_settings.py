from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    delivery_date_automation = fields.Selection(
        related="company_id.delivery_date_automation",
        readonly=False,
    )
    delivery_date_timezone = fields.Selection(
        related="company_id.delivery_date_timezone",
        readonly=False,
    )
    delivery_date_time_cutoff = fields.Float(
        related="company_id.delivery_date_time_cutoff",
        readonly=False,
    )
    delivery_date_default_weekdays = fields.Integer(
        related="company_id.delivery_date_default_weekdays",
        readonly=False,
    )
