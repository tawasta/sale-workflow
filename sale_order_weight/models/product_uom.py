# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ProductUom(models.Model):

    # 1. Private attributes
    _inherit = 'product.uom'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.multi
    def _compute_weight(self, weight, to_unit):
        if len(self) == 0:
            return 0

        self.ensure_one()

        if not self or not weight or not to_unit or self == to_unit:
            return weight

        if self.category_id.id != to_unit.category_id.id:
            return weight

        uom_weight = weight * self.factor

        if to_unit:
            uom_weight = uom_weight / to_unit.factor

        return uom_weight

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
