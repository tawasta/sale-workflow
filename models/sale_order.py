# -*- coding: utf-8 -*-
from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    customer_contact = fields.Many2one(
        'res.partner', "Customers contact",
    )

    @api.onchange('partner_invoice_id')
    def onchange_partner_invoice_id(self):
        self.customer_contact = self.env['res.partner'].search([
            ('parent_id', '=', self.partner_id.id),
        ], limit=1)
