from odoo import models

# sale_order field name, model name
check = {"partner_id": "res.partner"}


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, vals):
        for key in check:
            if key in vals:
                new_val = self.env[check[key]].search([("id", "=", vals[key])])
                if new_val.sale_warn_level == "blocking_warning":
                    del vals[key]
        return super().write(vals)
