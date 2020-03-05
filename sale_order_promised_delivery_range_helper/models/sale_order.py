from datetime import datetime

from odoo import fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SaleOrder(models.Model):

    _inherit = "sale.order"

    date_delivery_promised_days = fields.Integer(
        string="Promised delivery days", compute="_compute_date_delivery_promised"
    )

    date_delivery_promised_weeks = fields.Integer(
        string="Promised delivery weeks", compute="_compute_date_delivery_promised"
    )

    def _compute_date_delivery_promised(self):
        for record in self:
            start = record.date_delivery_promised_start
            end = record.date_delivery_promised_end

            if start and end:

                timespan = datetime.strptime(
                    end, DEFAULT_SERVER_DATE_FORMAT
                ) - datetime.strptime(start, DEFAULT_SERVER_DATE_FORMAT)

                days = timespan.days % 7
                weeks = timespan.days / 7

                record.date_delivery_promised_days = days
                record.date_delivery_promised_weeks = weeks
