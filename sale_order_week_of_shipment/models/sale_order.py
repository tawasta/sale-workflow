from odoo import fields, models, api
from datetime import datetime, date  # , timedelta


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _default_week_of_shipment(self):
        current_week = datetime.today().isocalendar()[1]
        additional_weeks = self.company_id.week_of_shipment_additional_weeks

        if additional_weeks > 0:
            return current_week + additional_weeks
        else:
            return current_week

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        default=_default_week_of_shipment,
        readonly=False,
    )

    @api.depends("commitment_date")
    @api.onchange("commitment_date")
    def _compute_week_of_shipment(self):
        for record in self:
            if record.commitment_date:
                week_from_date = date(
                    record.commitment_date.year,
                    record.commitment_date.month,
                    record.commitment_date.day
                ).isocalendar()[1]
                if week_from_date != record.week_of_shipment:
                    record.week_of_shipment = week_from_date
