# -*- coding: utf-8 -*-
from openerp import models, api, fields


class CrmCaseStage(models.Model):

    _inherit = 'crm.case.stage'

    sale_action = fields.Selection(selection='_get_sale_actions',
                                   inverse='_set_sale_action',
                                   string='Sale action')

    def _get_sale_actions(self):
        sale_actions = (
            ('quotation_send', 'Send quotation'),
            ('opportunity_won', 'Opportunity won'),
            ('opportunity_lost', 'Opportunity lost'),
        )

        return sale_actions

    @api.one
    def _set_sale_action(self):

        if self.sale_action == "quotation_send":

            ''' Unsetter unsets all lower sequence actions even when updating
            # Unset duplicate action variables with lower sequence
            records_unset = self.search([
                ('sale_action', '=', self.sale_action),
                ('sequence', '>', self.sequence),
            ])

            for record in records_unset:
                record.sale_action = False
            '''

            # Update all higher sequence actions
            records_update = self.search([
                ('sequence', '>=', self.sequence),
                ('sale_action', '=', False)],
                order='sequence ASC')

            for record in records_update:
                record.sale_action = self.sale_action

        else:
            # Unset any duplicate action variables
            records = self.search([
                ('sale_action', '=', self.sale_action),
                ('sale_action', '!=', 'False'),
                ('id', '!=', self.id)
            ])

            for record in records:
                record.sale_action = False
