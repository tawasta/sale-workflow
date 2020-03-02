# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields declaration
    next_delivery_date = fields.Date(
        string="Next delivery", compute="_compute_next_delivery_date", store=True
    )

    # 3. Default methods

    # 4. Compute and search fields
    @api.depends("picking_ids")
    def _compute_next_delivery_date(self):
        for record in self:
            if record.picking_ids:
                next_delivery_ids = record.picking_ids.filtered(
                    lambda r: r.state not in ("cancel", "done", "draft")
                ).sorted(key=lambda r: r.min_date)

                if next_delivery_ids:
                    record.next_delivery_date = next_delivery_ids[0].min_date

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
