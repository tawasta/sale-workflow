from odoo import _, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        for sale in self:
            if not sale.client_order_ref:
                msg = _("Please fill in the customer reference.")
                raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
