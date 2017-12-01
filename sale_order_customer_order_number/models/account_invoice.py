# -*- coding: utf-8 -*-
from odoo import models, fields, _


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    customer_order_number = fields.Char("Customer's Order Number", help='''If the customer has specified an order number of their own''')
