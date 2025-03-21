##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):
    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    def _prepare_invoice(self):
        # Add delivery date to values
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        date_delivered = False
        if self.effective_date:
            # The "correct" scenario: effective date is set
            date_delivered = self.effective_date
        elif self.commitment_date:
            # Fallback to commitment date
            if self.expected_date and self.expected_date > self.commitment_date:
                # Expected date is after commitment date.
                # Use expected date
                date_delivered = self.expected_date.date()
            else:
                date_delivered = self.commitment_date.date()
        elif self.expected_date:
            # No effective or commitment date. Fallback to expected date
            date_delivered = self.expected_date.date()

        if date_delivered:
            invoice_vals["date_delivered"] = date_delivered.isoformat()

        return invoice_vals
