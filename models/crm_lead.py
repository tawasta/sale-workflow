# -*- coding: utf-8 -*-
from openerp import models, api

import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    @api.multi
    def write(self, vals):
        ''' Extends default write to update sale order as the
        opportunity progresses '''

        if 'stage_id' in vals:
            sale_action = self.stage_id.browse(vals['stage_id']).sale_action
            if sale_action:
                self._update_sale_order(sale_action)

        return super(CrmLead, self).write(vals)

    @api.one
    def _update_sale_order(self, sale_action):
        ''' Updates sale order on opportunity action stages '''
        if sale_action == 'send_quotation':
            pass

        elif sale_action == 'opportunity_won':
            pass