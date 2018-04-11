# -*- coding: utf-8 -*-
from odoo import models, api, _

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = 'sale.order'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields
    @api.one
    def write(self, vals):
        # Extends default write to update opportunity as the sale progresses

        # Sale is confirmed. Mark the opportunity as won
        if 'state' in vals and vals['state'] == 'manual' and self.lead:
            self.lead.case_mark_won()

        # Update description to the lead
        if 'description' in vals and self.lead:
            self.lead.description = vals['description']

        return super(SaleOrder, self).write(vals)

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for record in self:
            opportunity = record.opportunity_id
            opportunity.message_post(_('Sale confirmed'))
            opportunity.action_set_won()

        return res

    @api.multi
    def action_set_lost(self):
        res = super(SaleOrder, self).action_cancel()

        for record in self:
            opportunity = record.opportunity_id
            opportunity.message_post(_('Sale canceled'))
            opportunity.action_set_won()

        return res

    # 8. Business methods
