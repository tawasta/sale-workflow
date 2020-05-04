import datetime

from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def compute_default_week_of_shipment(self):
        if self.week_of_shipment == 0 and self.expected_date:
            week_number = datetime.date(
                self.expected_date.year,
                self.expected_date.month,
                self.expected_date.day,
            ).isocalendar()[1]
            self.week_of_shipment = week_number
        else:
            self.week_of_shipment = 0

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=False,
        stored=True,
        computed="compute_default_week_of_shipment",
        default=0,
    )
