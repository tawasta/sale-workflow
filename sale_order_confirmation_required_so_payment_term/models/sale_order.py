from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for sale in self:
            if not sale.payment_term_id:
                raise UserError(_("Please fill in the payment term."))
        return super(SaleOrder, self).action_confirm()
