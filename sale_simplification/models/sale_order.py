# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp.exceptions import ValidationError
from openerp import _

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):
    # 1. Private attributes
    _inherit = 'sale.order'

    # 2. Fields declaration
    show_all = fields.Boolean(
        'Show all fields',
        help="Some of the lesser used fields are hidden by default"
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.one
    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            # Partner is a contact person
            if self.partner_id.type == 'contact'\
                    and not self.partner_id.is_company \
                    and self.partner_id.parent_id:
                self.customer_contact = self.partner_id
                self.partner_id = self.partner_id.parent_id

            self.partner_invoice_id = self.partner_id
            self.partner_shipping_id = self.partner_id

            self.pricelist_id = self.partner_id.property_product_pricelist
            self.currency_id = self.pricelist_id.currency_id
            self.payment_term = self.partner_id.property_payment_term

        super(SaleOrder, self).onchange_partner()

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_button_confirm(self):
        self.ensure_one()

        if self.partner_id.is_company and not self.partner_id.businessid:
            msg = _('Partner has no business id!')
            msg += "\n"
            msg += _('Please set a business id before confirming')

            raise ValidationError(msg)

        return super(SaleOrder, self).action_button_confirm()

    # 8. Business methods
