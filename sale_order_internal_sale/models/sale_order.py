# -*- coding: utf-8 -*-

# 1. Standard library imports:
#   import base64

# 2. Known third party imports (One per line sorted and splitted in python stdlib):
#   import lxml

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:
#   from . import utils

# 6. Unknown third party imports (One per line sorted and splitted in python stdlib):
#   _logger = logging.getLogger(__name__)

# Use camelcase for code in api v8 (class AccountInvoice), 
# underscore lowercase notation for old api (class account_invoice).

class SaleOrder(models.Model):
    # 1. Private attributes
    _inherit = 'sale.order'

    # 2. Fields declaration
    internal_sale = \
        fields.Boolean(
            'Internal sale',
            default=False,
            help="A sale within the company group. These sales will be given "
            + "an analytic account automatically",
            readonly=False,
            states={
                'manual': [('readonly', True)],
                'progress': [('readonly', True)],
                'done': [('readonly', True)],
            }
        )

    # 3. Default methods

    # 4. compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange('internal_sale')
    @api.depends('project_id')
    def onchange_internal_sale(self):
        analytic = self._get_account_internal_sale()

        if self.project_id and self.internal_sale:
            if not self.project_id.id == analytic.id:
                self.project_id.parent_project_id = analytic.id
        elif self.internal_sale and not self.project_id:
            self.project_id = analytic

    @api.onchange('project_id')
    @api.depends('internal_sale')
    def onchange_project_id(self):
        if not self.project_id:
            self.internal_sale = False

        analytic = self._get_account_internal_sale()

        if self.project_id.parent_project_id.id == analytic.id or self.project_id.id == analytic.id:
            self.internal_sale = True
        else:
            self.internal_sale = False

    # 6. CRUD methods
    @api.one
    def write(self, vals):
        super(SaleOrder, self).write(vals)

        if self.project_id and self.internal_sale:
            analytic = self._get_account_internal_sale()

            if not self.project_id.id == analytic.id:
                self.project_id.parent_project_id = analytic.id

    # 7. Action methods

    # 8. Business methods
    def _get_account_internal_sale(self):
        analytic_account = self.project_id.sudo().search(
            [('code', 'like', 'INTSAL'),
             ('company_id', '=', self.company_id.id)],
            limit=1,
        )

        return analytic_account
