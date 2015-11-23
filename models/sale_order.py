# -*- coding: utf-8 -*-
from openerp import models, api, fields

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = 'sale.order'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.one
    def write(self, vals):
        ''' Extends default write to update opportunity as the
        sale progresses '''

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

    # 8. Business methods
