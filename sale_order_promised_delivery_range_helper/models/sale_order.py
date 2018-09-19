# -*- coding: utf-8 -*-
from odoo import models, fields
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    date_delivery_promised_days = fields.Integer(
        string='Promised delivery days',
        compute='_compute_date_delivery_promised_length',
    )

    date_delivery_promised_weeks = fields.Integer(
        string='Promised delivery weeks',
        compute='_compute_date_delivery_promised_length',
    )

    def _compute_date_delivery_promised_length(self):
        for record in self:
            start = record.date_delivery_promised_start
            end = record.date_delivery_promised_end

            if start and end:

                length = \
                    datetime.strptime(end, DEFAULT_SERVER_DATE_FORMAT) -\
                    datetime.strptime(start, DEFAULT_SERVER_DATE_FORMAT)

                days = length.days % 7
                weeks = length.days / 7

                record.date_delivery_promised_days = days
                record.date_delivery_promised_weeks = weeks
