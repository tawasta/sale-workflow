from odoo import _, api, exceptions, models


class SaleOrderMassCancel(models.TransientModel):
    _name = "sale.order.mass.cancel"

    def get_cancellable_states(self):
        return ["draft", "sent", "sale"]

    @api.multi
    def confirm(self):

        sale_orders = self.env["sale.order"].browse(self._context.get("active_ids"))

        allowed_states = self.get_cancellable_states()

        if any(s.state not in allowed_states for s in sale_orders):
            msg = _("Please select only quotations whose states " "allow cancelling")
            raise exceptions.UserError(msg)

        for sale_order in sale_orders:
            sale_order.action_cancel()
