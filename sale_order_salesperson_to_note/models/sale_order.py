from odoo import _, api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        # Add salesperson to sale note
        for order in self:
            if order.user_id:

                salesperson = _("Salesperson: %s") % order.user_id.name

                if order.note:
                    order.note = salesperson + "\n" + order.note
                else:
                    order.note = salesperson

        return res
