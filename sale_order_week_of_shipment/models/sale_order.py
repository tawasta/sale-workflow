from odoo import fields, models, api
import datetime


class SaleOrder(models.Model):

    _inherit = "sale.order"

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        compute="_compute_week_of_shipment",
        readonly=False
    )

    @api.depends("expected_date")
    def _compute_week_of_shipment(self):
        for record in self:
            if record.expected_date:
                record.week_of_shipment = datetime.date(
                    record.expected_date.year,
                    record.expected_date.month,
                    record.expected_date.day
                ).isocalendar()[1]
            else:
                record.week_of_shipment = 0
