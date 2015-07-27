# -*- coding: utf-8 -*-
from openerp import models, api, fields


class CrmCaseStage(models.Model):

    _inherit = 'crm.case.stage'

    sale_action = fields.Selection(selection='_get_sale_actions',
                                   inverse='_set_sale_action',
                                   string='Sale action')

    def _get_sale_actions(self):
        sale_actions = (
            ('send_quotation', 'Send quotation'),
            ('opportunity_won', 'Opportunity won'),
            ('opportunity_lost', 'Opportunity lost'),
        )

        return sale_actions

    @api.one
    def _set_sale_action(self):
        # Unsets any duplicate action variables

        records = self.search([('sale_action', '=', self.sale_action),
                               ('sale_action', '!=', 'False'),
                               ('id', '!=', self.id)])

        for record in records:
            record.sale_action = False
