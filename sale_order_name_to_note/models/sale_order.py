from odoo import _, api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        # Add name (order reference) to sale note
        for order in self:
            if order.name:

                reference = _("Our reference: %s") % order.name

                if order.note:
                    order.note = reference + "\n" + order.note
                else:
                    order.note = reference

        return res
