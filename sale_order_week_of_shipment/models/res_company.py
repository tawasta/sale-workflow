from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    week_of_shipment_additional_weeks = fields.Integer(
        string="Additional weeks to default week of shipment date(today)",
        default=0,
    )

    week_of_shipment_force_additional_weeks = fields.Boolean(
        string="Force additional weeks to week of shipment",
        help="""Dont let user set the value lower than default(today)
            plus additional weeks""",
        default=False,
    )

    week_of_shipment_additional_weeks_group = fields.Many2one(
        string="Apply additional weeks rule to only this group",
        comodel_name="res.groups",
    )
