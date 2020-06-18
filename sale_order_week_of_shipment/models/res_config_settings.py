from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    week_of_shipment_additional_weeks = fields.Integer(
        string="Additional week to default week of shipment date(todays week)",
        related="company_id.week_of_shipment_additional_weeks",
        help="Number of weeks to be added to default value which is todays week",
        readonly=False,
    )

    week_of_shipment_force_additional_weeks = fields.Boolean(
        string="Force additional weeks to week of shipment",
        related="company_id.week_of_shipment_force_additional_weeks ",
        help="""Dont let user set the value lower than default(todays weeks)
            plus additional weeks""",
        readonly=False,
    )

    week_of_shipment_additional_weeks_group = fields.Many2one(
        string="Apply additional weeks rule to only this group",
        related="company_id.week_of_shipment_additional_weeks_group",
        readonly=False,
    )
