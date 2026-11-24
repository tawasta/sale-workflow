from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _notify_get_recipients_groups(self, message, model_description, msg_vals=False):
        groups = super()._notify_get_recipients_groups(
            message, model_description, msg_vals=msg_vals
        )
        # Replaces the "Accept & Sign Quotation" label of the email button; the
        # button still opens the quotation, where the customer accepts and signs.
        if not self or not self._has_to_be_signed() or self._has_to_be_paid():
            return groups
        for group in groups:
            if group[0] == "portal_customer" and group[2].get("button_access"):
                group[2]["button_access"]["title"] = self.env._("View Quotation")
        return groups
