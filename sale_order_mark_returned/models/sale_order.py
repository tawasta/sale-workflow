# -*- coding: utf-8 -*-
from openerp import models, fields, api, _, exceptions


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    returned = fields.Boolean('Returned', help='''Products have been shipped but then returned by the customer.''')