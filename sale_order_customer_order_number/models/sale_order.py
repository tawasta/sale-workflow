# -*- coding: utf-8 -*-
from openerp import models, fields, _
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    customer_order_number = fields.Char("Customer's Order Number", help='''If the customer has specified an order number of their own''')
