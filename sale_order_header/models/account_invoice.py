# -*- coding: utf-8 -*-
from odoo import models, fields, _


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    header_text = fields.Char('Header', help='Header or title of the Invoice')