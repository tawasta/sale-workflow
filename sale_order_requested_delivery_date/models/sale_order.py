# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    date_delivery_requested = fields.Datetime(
        string='Requested Delivery Date',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
        help='''Delivery date requested by the customer'''
    )
