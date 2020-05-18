from odoo import fields, models, api
import datetime


class SaleOrder(models.Model):

    _inherit = "sale.order"

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        compute="_compute_week_of_shipment",
        readonly=False,
        store=True
    )

    @api.depends("week_of_shipment", "date_order")
    def _compute_week_of_shipment(self):
        for record in self:
            if record.date_order:
                record.week_of_shipment = datetime.date(
                    self.date_order.year,
                    self.date_order.month,
                    self.date_order.day
                ).isocalendar()[1]
