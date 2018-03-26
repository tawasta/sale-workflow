# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports

# 3. Odoo imports (openerp):
from openerp import api, models

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports


class SaleOrder(models.Model):

    # Variable names:
    # Use underscore lowercase notation for common variable (snake_case)
    # since new API works with record or recordset instead of id list,
    # don't suffix variable name with _id or _ids if they do not contain
    # an id or a list of ids.

    # Constants:
    # Use underscore uppercase notation for global variables or constants.

    # 1. Private attributes
    _inherit = 'sale.order'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.one
    def action_create_contract(self):
        vals = {
            'name': 'Contract: %s (%s)' % (self.partner_id.name, self.name),
            'partner_id': self.partner_id.id,
            'type': 'contract',
        }

        contract = self.project_id.create(vals)

        for order_line in self.order_line:
            vals = {
                'name':         order_line.name,
                'price_unit':   order_line.price_unit,
                'uom_id':       order_line.product_uom.id,
                'quantity':     order_line.product_uom_qty,
                'product_id':   order_line.product_id.id,
            }
            contract.write({'recurring_invoice_line_ids': [(0, 0, vals)]})

        self.project_id = contract.id

    # 8. Business methods
