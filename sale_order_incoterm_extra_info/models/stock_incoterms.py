# -*- coding: utf-8 -*-
from openerp import models, fields, api, _, exceptions


class StockIncoterms(models.Model):

    _inherit = 'stock.incoterms'

    append_partner_name = fields.Boolean('Show Customer in Extra Info', default=False, help='''Adds the customer shipping address to Incoterm Extra Info field on Sale Order''')