# -*- coding: utf-8 -*-

# 1. Standard library imports:
from datetime import date
from dateutil.relativedelta import relativedelta

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):
    
    # 1. Private attributes
    _inherit = 'sale.order'

    # 2. Fields declaration
    date_validity = fields.Date(
        'Validity date',
        default=lambda self: self._default_date_validity()
    )

    # 3. Default methods
    def _default_date_validity(self):
        # Default validity is two months
        # TODO: get validity from config
        date_validity = date.today() + relativedelta(months=2)
        return date_validity

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
