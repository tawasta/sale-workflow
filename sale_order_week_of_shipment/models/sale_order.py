from odoo import fields, models, api
from datetime import datetime, date, timedelta


class SaleOrder(models.Model):

    _inherit = "sale.order"

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=False,
        store=True
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

    @api.depends("week_of_shipment")
    @api.onchange("week_of_shipment")
    def _compute_comitment_date(self):
        for record in self:
            week_from_date = 0
            if record.commitment_date:
                week_from_date = date(
                    record.commitment_date.year,
                    record.commitment_date.month,
                    record.commitment_date.day
                ).isocalendar()[1]

            if record.week_of_shipment > 0 and record.week_of_shipment < 53:
                if week_from_date != record.week_of_shipment:
                    weeks = record.week_of_shipment
                    days_in_week = 7
                    nth_day = weeks * days_in_week - days_in_week
                    current_year = datetime.now().year
                    start_of_year = datetime(current_year, 1, 1)
                    record.commitment_date = start_of_year + timedelta(days=nth_day)
            else:
                self._compute_week_of_shipment()
