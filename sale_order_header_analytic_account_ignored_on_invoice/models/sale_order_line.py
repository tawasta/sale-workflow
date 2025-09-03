from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _set_analytic_distribution(self, inv_line_vals, **optional_values):
        """Removed the functionality to add analytic account from sale order header"""
        if self.analytic_distribution and not self.display_type:
            inv_line_vals["analytic_distribution"] = self.analytic_distribution
