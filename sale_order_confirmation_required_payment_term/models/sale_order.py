from odoo import _, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):

        for sale in self:

            # Ignore orders autoconfirmed from website
            from_website = hasattr(sale, "website_id") and sale.website_id

            if not from_website and not sale.partner_id.property_payment_term_id:
                msg = (
                    _(
                        "Please fill in the customer payment terms for the "
                        "customer %s."
                    )
                    % sale.partner_id.name
                )
                raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
