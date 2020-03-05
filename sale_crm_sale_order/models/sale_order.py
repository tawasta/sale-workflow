import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for record in self:
            if record.opportunity_id:
                opportunity = record.opportunity_id
                opportunity.message_post(_("Sale confirmed"))
                opportunity.action_set_won()

        return res

    @api.multi
    def action_set_lost(self):
        res = super(SaleOrder, self).action_cancel()

        for record in self:
            if record.opportunity_id:
                opportunity = record.opportunity_id
                opportunity.message_post(_("Sale cancelled"))
                opportunity.action_set_won()

        return res
