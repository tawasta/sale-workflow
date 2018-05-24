# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil import parser


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    date_delivery_promised_start = fields.Date(
        string='Promised Delivery start',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
        copy=False,
    )

    date_delivery_promised_end = fields.Date(
        string='Promised Delivery end',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
        copy=False,
    )

    @api.onchange('date_delivery_promised_start')
    def onchange_date_delivery_start_update_date_delivery_end(self):
        for record in self:
            start = record.date_delivery_promised_start
            end = record.date_delivery_promised_end

            if not end or end < start:
                record.date_delivery_promised_end = start

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        # Add delivery range to sale note
        for order in self:
            if order.date_delivery_promised_start:

                # TODO: use user format?
                date_format = '%d.%m.%Y'

                start = parser.parse(order.date_delivery_promised_start)
                date_range = start.strftime(date_format)

                end = parser.parse(order.date_delivery_promised_end)

                if end:
                    date_range = '%s - %s' \
                                 % (date_range, end.strftime(date_format))

                delivery = '%s: %s\n' % (_('Delivery'), date_range)

                if order.note:
                    order.note += '\n' + delivery
                else:
                    order.note = delivery


        return res
