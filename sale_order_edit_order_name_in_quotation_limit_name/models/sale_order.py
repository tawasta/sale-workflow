from odoo import _, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def check_name_length(self, name):
        return len(name) > 13

    def write(self, values):
        res = super().write(values)

        name = values.get("name", False)
        if name:
            name_too_long = self.check_name_length(name)
            if name_too_long:
                raise ValidationError(
                    _("Sale Order name should not exceed 13 characters.")
                )

        return res
