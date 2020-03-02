# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class StockPicking(models.Model):

    # 1. Private attributes
    _inherit = "stock.picking"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.multi
    def write(self, values):
        res = super(StockPicking, self).write(values)

        if "state" in values or "min_date" in values or "recompute_pack_op" in values:

            # When delivery is changed, update SO
            self._compute_sale_order_next_delivery_date()

        return res

    # 7. Action methods
    @api.multi
    def action_confirm(self):
        res = super(StockPicking, self).action_confirm()

        self._compute_sale_order_next_delivery_date()

        return res

    @api.multi
    def action_cancel(self):
        res = super(StockPicking, self).action_cancel()

        self._compute_sale_order_next_delivery_date()

        return res

    @api.multi
    def action_assign(self):
        res = super(StockPicking, self).action_assign()

        self._compute_sale_order_next_delivery_date()

        return res

    @api.multi
    def force_assign(self):
        res = super(StockPicking, self).force_assign()

        self._compute_sale_order_next_delivery_date()

        return res

    @api.multi
    def action_done(self):
        res = super(StockPicking, self).action_done()

        self._compute_sale_order_next_delivery_date()

        return res

    # 8. Business methods
    def _compute_sale_order_next_delivery_date(self):
        for record in self:
            if record.sale_id:
                record.sale_id.compute_next_delivery_date()
