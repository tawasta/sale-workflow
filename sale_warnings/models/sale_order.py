from odoo import api, fields, models
from odoo.exceptions import ValidationError

# sale_order field name, model name
check = {"partner_id": "res.partner"}


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_sale_warn_level = fields.Selection(related="partner_id.sale_warn_level")

    @api.onchange("partner_id")
    def _onchange_customer_partner(self):
        if (
            self.partner_id.sale_warn_level == "popup_warning"
            and self.partner_id.sale_warn_msg
        ):
            return {
                "warning": {
                    "title": self.env._("Warning from customer!"),
                    "message": self.partner_id.sale_warn_msg,
                }
            }

    def write(self, vals):
        for key in check:
            if key in vals:
                new_val = self.env[check[key]].search([("id", "=", vals[key])])
                if new_val.sale_warn_level == "blocking_warning":
                    msg = self.env._(
                        "Blocked: customer has a blocking warning to prevent saving!"
                    )
                    raise ValidationError(msg)
                    # del vals[key]
        return super().write(vals)
