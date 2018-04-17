# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import models, fields, api

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = 'sale.order'

    _FIELD_STATES = {
        'draft': [('readonly', False)],
        'sent': [('readonly', False)],
        'manual': [('readonly', False)],
    }

    # 2. Fields declaration
    customer_contact = fields.Many2one(
        'res.partner', "Contact",
        states=_FIELD_STATES,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.multi
    @api.onchange('partner_id')
    def onchange_partner(self):
        self.ensure_one()

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

    @api.multi
    @api.onchange('partner_id')
    @api.depends('customer_contact')
    def onchange_partner_domain_change(self):
        # Get the contact domain
        res = dict()
        if self.partner_id:
            top_parent_list = self.partner_id._get_recursive_parent()

            if top_parent_list:
                top_parent = top_parent_list[0]
                partners = self.partner_id \
                    ._get_recursive_child_ids(top_parent) + [top_parent.id]

                contacts = self.env['res.partner'].search([
                    ('id', 'in', partners),
                    ('type', '=', 'contact'),
                    ('is_company', '=', False)
                ])

                if contacts:
                    domain = [
                        ('id', 'in', contacts.ids),
                    ]
                    res['domain'] = {'customer_contact': domain}

        return res

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def _prepare_invoice(self):
        # Handling for when invoicing the invoiceable lines
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['customer_contact'] \
            = self.customer_contact and self.customer_contact.id or False
        return invoice_vals
