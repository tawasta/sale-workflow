# -*- coding: utf-8 -*-
from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    _FIELD_STATES = {
        'draft': [('readonly', False)],
        'sent': [('readonly', False)],
        'manual': [('readonly', False)],
    }

    customer_contact = fields.Many2one(
        'res.partner', "Customers contact",
        states=_FIELD_STATES
    )

    @api.onchange('partner_invoice_id')
    def onchange_partner_invoice_id(self):
        self.customer_contact = self.partner_id.search([
            ('parent_id', '=', self.partner_id.id),
            ('type', '=', 'contact'),
            ('is_company', '=', False),
        ], limit=1)
