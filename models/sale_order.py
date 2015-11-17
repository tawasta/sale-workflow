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
            partner = self.partner_id

            # Partner is a contact person
            if partner.type == 'contact'\
                    and not partner.is_company \
                    and partner.parent_id:
                self.customer_contact = partner
                self.partner_id = partner.parent_id

            self.partner_invoice_id = partner
            self.partner_shipping_id = partner

            self.pricelist_id = partner.property_product_pricelist
            self.currency_id = self.pricelist_id.currency_id
            self.payment_term = partner.property_payment_term

        super(SaleOrder, self).onchange_partner()

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
