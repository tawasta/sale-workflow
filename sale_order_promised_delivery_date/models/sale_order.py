# -*- coding: utf-8 -*-
from openerp import models, fields, api, _, exceptions


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    date_delivery_promised = fields.Date('Promised Delivery Date', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})