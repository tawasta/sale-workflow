from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)

        if vals.get("partner_id"):
            user_id = vals.get("partner_id")
            if vals.get("partner_id") != self.env.ref("base.public_partner").id:
                vals["fiscal_position_id"] = (
                    self.env["res.partner"]
                    .search([("id", "=", int(user_id))])
                    .property_account_position_id.id
                )

        return res
