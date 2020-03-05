# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

from odoo.addons import decimal_precision as dp

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields declaration
    weight = fields.Float(
        "Weight", digits=dp.get_precision("Stock Weight"), compute="_compute_weight"
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_weight(self):
        for record in self:
            weight = 0
            for line in record.order_line:
                weight += line.weight

            record.weight = weight

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
