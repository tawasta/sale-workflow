# -*- coding: utf-8 -*-
from odoo import models, api, exceptions, _


class ConfirmWizard(models.TransientModel):

    _name = "sale_order_confirm_multiple.confirm_wizard"

    def get_confirmable_states(self):
        return ['draft', 'sent']

    @api.multi
    def confirm(self):

        sale_orders \
             = self.env['sale.order'].browse(self._context.get('active_ids'))

        allowed_states = self.get_confirmable_states()

        if any(s.state not in allowed_states for s in sale_orders):
            msg = _('Please select only quotations whose states '
                    'allow confirming')
            raise exceptions.UserError(msg)

        for sale_order in sale_orders:
            sale_order.action_confirm()
