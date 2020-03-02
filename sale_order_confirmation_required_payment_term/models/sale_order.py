from odoo import _, api, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        for sale in self:
            if not sale.partner_id.property_payment_term_id:
                msg = (
                    _(
                        "Please fill in the customer payment terms for the "
                        "customer %s."
                    )
                    % sale.partner_id.name
                )
                raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
