from odoo import _, api, models
from odoo.exceptions import AccessError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_unlock(self):
        # Unlock sales

        # Only allow sales manager to use this
        if not self.env.user.has_group("sales_team.group_sale_manager"):
            msg = _("Unlocking is only allowed for sales managers")
            raise AccessError(msg)

        for record in self:
            record.state = "sale"
