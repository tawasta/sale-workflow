# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules (rarely, and only if necessary):

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
    show_all = fields.Boolean(
        'Show all fields',
        help="Some of the lesser used fields are hidden by default"
    )

    # Allow modifying fields until the invoice is created
    partner_id = fields.Many2one(states=_FIELD_STATES)
    partner_invoice_id = fields.Many2one(states=_FIELD_STATES)
    partner_shipping_id = fields.Many2one(states=_FIELD_STATES)

    date_order = fields.Datetime(states=_FIELD_STATES)
    order_line = fields.One2many(states=_FIELD_STATES)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.one
    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            # Partner is a contact person
            if self.partner_id.type == 'contact'\
                    and not self.partner_id.is_company:
                self.customer_contact = self.partner_id
                self.partner_id = self.partner_id.parent_id

            self.partner_invoice_id = self.partner_id
            self.partner_shipping_id = self.partner_id

        super(SaleOrder, self).onchange_partner()

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
