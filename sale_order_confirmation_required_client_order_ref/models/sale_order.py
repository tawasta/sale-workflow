from odoo import _, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):

        # Don't enforce the check on autoconfirmed website sales
        from_website = self._context.get("website_id", False)

        if not from_website:
            for sale in self:
                if not sale.client_order_ref:
                    msg = _("Please fill in the customer reference.")
                    raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
