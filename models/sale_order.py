# -*- coding: utf-8 -*-
from openerp import models, api

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.one
    def write(self, vals):
        ''' Extends default write to update opportunity as the
        sale progresses '''

        if 'state' in vals and vals['state'] == 'manual' and self.lead:
            # Sale is confirmed. Mark the opportunity as won
            self.lead.case_mark_won()

        if 'description' in vals and self.lead:
            self.lead.description = vals['description']

        return super(SaleOrder, self).write(vals)
