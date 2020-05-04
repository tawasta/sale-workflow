import datetime

from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def compute_default_week_of_shipment(self):
        week_number = datetime.date(
            self.expected_date.year, self.expected_date.month, self.expected_date.day
        ).isocalendar()[1]
        self.week_of_shipment = week_number

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=False,
        computed="compute_default_week_of_shipment",
    )
