# -*- coding: utf-8 -*-
from openerp import models, api

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def write(self, vals):
        ''' Extends default write to update opportunity as the
        sale progresses '''

        if 'state' in vals and vals['state'] == 'manual' and self.lead_id:
            # Sale is confirmed. Mark the opportunity as won
            self.lead_id.case_mark_won()

        if 'description' in vals and self.lead_id:
            self.lead_id.description = vals['description']

        return super(SaleOrder, self).write(vals)
