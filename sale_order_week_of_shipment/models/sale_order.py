from odoo import fields, models
import datetime


class SaleOrder(models.Model):

    _inherit = "sale.order"

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=False,
        compute="compute_week_of_shipment",
        stored=True
    )

    _previous_week_of_shipment_value = fields.Integer()

    def compute_week_of_shipment(self):
        if self.expected_date:
            if self._previous_week_of_shipment_value == 0:
                self.week_of_shipment = datetime.date(
                    self.expected_date.year,
                    self.expected_date.month,
                    self.expected_date.day
                ).isocalendar()[1]
                self._previous_week_of_shipment_value = self.week_of_shipment
