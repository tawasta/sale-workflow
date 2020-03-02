from odoo import _, api, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        for sale in self:
            if (
                sale.partner_id.company_type == "company"
                and not sale.partner_id.business_id
            ):
                msg = (
                    _("Please fill in business ID for the customer %s.")
                    % sale.partner_id.name
                )
                raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
