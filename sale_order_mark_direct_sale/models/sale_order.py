# -*- coding: utf-8 -*-
from openerp import models, fields, api, _, exceptions


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    direct_sale = fields.Boolean('Direct Sale')