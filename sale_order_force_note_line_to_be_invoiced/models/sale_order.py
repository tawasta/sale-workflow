##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    def _create_invoices(self, grouped=False, final=False, date=None):
        # Force line notes to invoice
        for order in self:
            for line in order.order_line:
                if line.display_type and line.display_type == "line_note":
                    # Set lines to be invoiced
                    # They will reset to 0 when "to invoice" compute triggers
                    line.qty_to_invoice = 1
        return super()._create_invoices(grouped, final, date)

    # 8. Business methods
