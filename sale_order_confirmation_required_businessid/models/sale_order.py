from odoo import _, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):

        for sale in self:

            # Ignore orders autoconfirmed from website
            from_website = hasattr(sale, "website_id") and sale.website_id

            if (
                not from_website
                and sale.partner_id.company_type == "company"
                and not sale.partner_id.business_code
            ):
                msg = (
                    _("Please fill in business ID for the customer %s.")
                    % sale.partner_id.name
                )
                raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
