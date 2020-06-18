from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    week_of_shipment_additional_weeks = fields.Integer(
        string="Additional weeks to default week of shipment date(today)",
        default=0,
    )

    week_of_shipment_additional_weeks_group = fields.Many2one(
        string="Apply additional weeks rule to only this group",
        comodel_name="res.groups",
    )
