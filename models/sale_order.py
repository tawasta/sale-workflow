# -*- coding: utf-8 -*-
from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    show_all = fields.Boolean(
        'Show all fields',
        help="Some of the lesser used fields are hidden by default"
    )
