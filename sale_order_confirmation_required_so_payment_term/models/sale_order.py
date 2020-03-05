from odoo import _, api, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        for sale in self:
            if not sale.payment_term_id:
                msg = _("Please fill in the payment term.")
                raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
