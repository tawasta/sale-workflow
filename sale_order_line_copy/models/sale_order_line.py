# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrderLine(models.Model):

    # 1. Private attributes
    _inherit = "sale.order.line"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_sale_order_line_copy(self):
        self.ensure_one()

        self.copy({"order_id": self.order_id.id})
        return {"type": "ir.actions.client", "tag": "reload"}

    # 8. Business methods
