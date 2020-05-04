import datetime

from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def compute_default_week_of_shipment(self):
        if (
            isinstance(self.expected_date, datetime.datetime)
            and self.week_of_shipment == 0
        ):
            week_number = datetime.date(
                self.expected_date.year,
                self.expected_date.month,
                self.expected_date.day,
            ).isocalendar()[1]
            if week_number.isdigit():
                self.week_of_shipment = week_number
            else:
                self.week_of_shipment = 0
        else:
            self.week_of_shipment = 0

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=False,
        stored=True,
        computed="compute_default_week_of_shipment",
        default=0,
    )
