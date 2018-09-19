# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrderLine(models.Model):

    # 1. Private attributes
    _inherit = 'sale.order.line'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        # Don't auto-update anything when price is changed
        if self._context.get('quantity'):
            return

        return super(SaleOrderLine, self).product_uom_change()

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
