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
        'res.partner', "Contact",
        states=_FIELD_STATES
    )

    @api.one
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        # Don't get a contact if there is no partner
        if not self.partner_id:
            return False

        # Contact is already set
        if self.customer_contact.parent_id == self.partner_id:
            return False

        self.customer_contact = self.partner_id.search([
            ('parent_id', '=', self.partner_id.id),
            ('type', '=', 'contact'),
            ('is_company', '=', False),
        ], limit=1)
