# -*- coding: utf-8 -*-
from odoo import api, models


class AccountAnalyticAccount(models.Model):
    # 1. Private attributes
    _inherit = 'account.analytic.account'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    ''' When the module is installed,
    fetch all companies and create analytic accounts '''
    @api.model
    def _init_analytic_accounts(self):
        companies = self.company_id.search([])

        for company in companies:
            self._create_analytic_accounts(company)

    def _create_analytic_accounts(self, company):
        company_code = company.name.replace(" ", "")[:5].upper()

        vals = {
            'id': company_code,
            'external_id': company_code,
            'company_id': company.id,
            'name': company.name,
            'code': company_code,
            'type': 'view',
        }

        parent = self.create(vals)

        code = 'INTSAL_%s' % company_code

        vals = {
            'id': code,
            'external_id': code,
            'company_id': company.id,
            'name': 'Internal Sales',
            'code': code,
            'parent_id': parent.id,
            'type': 'normal',
        }

        self.create(vals)
