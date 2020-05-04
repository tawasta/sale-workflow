import datetime

from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def compute_default_week_of_shipment(self):
        if isinstance(self.expected_date, datetime.datetime):
            week_number = datetime.date(
                self.expected_date.year,
                self.expected_date.month,
                self.expected_date.day,
            ).isocalendar()[1]
            if week_number.isdigit():
                return week_number
            else:
                return 0
        else:
            return 0

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=False,
        default=compute_default_week_of_shipment,
    )
