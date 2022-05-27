
from odoo import api, exceptions, models


class SaleOrderGlobalDiscount(models.TransientModel):

    _name = "sale.order.global.discount"

    def get_confirmable_states(self):
        return {"draft": "Draft"}

    @api.multi
    def compute_global_discount(self):
        """ Computes Global discount for selected sale orders. """
        orders = self.env["sale.order"].browse(self._context.get("active_ids"))

        allowed_states = self.get_confirmable_states()

        if any(s.state not in allowed_states.keys() for s in orders):
            states = ', '.join(list(allowed_states.values()))
            msg = ("Please only select sale orders in %s state") % states
            raise exceptions.UserError(msg)

        for order in orders:
            order.compute_global_discount()
