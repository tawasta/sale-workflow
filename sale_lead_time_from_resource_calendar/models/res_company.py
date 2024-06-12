from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    sale_lead_time_resource_calendar_id = fields.Many2one(
        string="Resource Calendar for Calculating Sale Lead Times",
        comodel_name="resource.calendar",
    )
