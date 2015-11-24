# -*- coding: utf-8 -*-

# 1. Standard library imports:
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp.exceptions import ValidationError

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
        # Get the order date in correct format
        date_order = datetime.strptime(self.date_order[:10], "%Y-%m-%d") \
            if self.date_order \
            else date.today()

        # Default validity is two months
        # TODO: get validity from config
        date_validity = date_order + relativedelta(months=2)

        # Return date as a string
        date_validity = date_validity.strftime('%Y-%m-%d')

        return date_validity

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.one
    @api.onchange('date_order')
    def _onchange_date_order(self):
        self.date_validity = self._default_date_validity()

    @api.one
    @api.constrains('date_validity')
    def _check_date_validity(self):
        if self.date_order > self.date_validity:
            raise ValidationError("Validity date can't be before order date")

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
