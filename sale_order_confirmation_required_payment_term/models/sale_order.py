from odoo import _, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):

        # Don't enforce the check on autoconfirmed website sales
        from_website = self._context.get("website_id", False)

        if not from_website:
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
