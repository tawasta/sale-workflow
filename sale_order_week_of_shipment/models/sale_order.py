from odoo import fields, models
import datetime


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def compute_week_of_shipment(self):
        if self.expected_date:
            datetime.date(
                self.expected_date.year,
                self.expected_date.month,
                self.expected_date.day
            ).isocalendar()[1]
        else:
            return 0

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        default=compute_week_of_shipment,
        compute="temp_compute",
        stored=True
    )

    def temp_compute(self):
        if self.week_of_shipment == 0 and self.expected_date:
            self.week_of_shipment = self.compute_week_of_shipment()
