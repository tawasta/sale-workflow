# -*- coding: utf-8 -*-
from openerp import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    customer_contact = fields.Many2one('res.partner', "Customer's contact")
