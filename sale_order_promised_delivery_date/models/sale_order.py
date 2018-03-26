# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    date_delivery_promised = fields.Date(
        string='Promised Delivery Date',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        }
    )
