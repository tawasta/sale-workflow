# -*- coding: utf-8 -*-

# 1. Standard library imports:
#   import base64

# 2. Known third party imports (One per line sorted and splitted in python stdlib):
#   import lxml

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules (rarely, and only if necessary):
#   from openerp.addons.website.models.website import slug

# 5. Local imports in the relative form:
#   from . import utils

# 6. Unknown third party imports (One per line sorted and splitted in python stdlib):
#   _logger = logging.getLogger(__name__)

# Use camelcase for code in api v8 (class AccountInvoice), 
# underscore lowercase notation for old api (class account_invoice).

class AccountAnalyticAccount(models.Model):
    # 1. Private attributes
    _inherit = 'account.analytic.account'
    
    # 2. Fields declaration

    # 3. Default methods

    # 4. compute and search fields, in the same order that fields declaration
   
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
