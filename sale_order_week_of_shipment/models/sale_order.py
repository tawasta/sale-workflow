import datetime

from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=False,
        default="_compute_default_week_of_shipment",
    )

    def _compute_default_week_of_shipment(self):
        if self.expected_date:
            return datetime.date(
                self.expected_date.year,
                self.expected_date.month,
                self.expected_date.day,
            ).isocalendar()[1]
        else:
            return 0
