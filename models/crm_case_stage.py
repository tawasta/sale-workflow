# -*- coding: utf-8 -*-
from openerp import models, fields


class CrmCaseStage(models.Model):

    _inherit = 'crm.case.stage'

    sale_action = fields.Selection(selection='_get_sale_actions',
                                   string='Sale action')

    def _get_sale_actions(self):
        sale_actions = (
            ('send_quotation', 'Send quotation'),
            ('confirm_sale', 'Confirm quotation'),
        )

        return sale_actions
