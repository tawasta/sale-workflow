# -*- coding: utf-8 -*-

# 1. Standard library imports:
#	import base64

# 2. Known third party imports (One per line sorted and splitted in python stdlib):
#	import lxml

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules (rarely, and only if necessary):
#	from openerp.addons.website.models.website import slug

# 5. Local imports in the relative form:
#	from . import utils

# 6. Unknown third party imports (One per line sorted and splitted in python stdlib):
#	_logger = logging.getLogger(__name__)

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
            readonly=True,
            states={'draft': [('readonly', False)]},
        )

    # 3. Default methods
    # def _default_name(self):


    # 4. compute and search fields, in the same order that fields declaration
    # @api.multi
    # @api.depends('seats_max', 'registration_ids.state')
    # def _compute_seats(self):
   

    # 5. Constraints and onchanges
    # @api.constrains('seats_max', 'seats_available')
    # def _check_seats_limit(self):
      
    @api.onchange('internal_sale')
    @api.depends('name', 'project_id')
    def _onchange_internal_sale(self):
        if self.internal_sale and not self.project_id:
            vals = {}
            vals['name'] = self.partner_id.name
            vals['type'] = 'view'
            vals['parent_id'] = self.project_id.sudo().search([('code','=','INTSAL')]).id
            vals['partner_id'] = self.partner_id.id

            analytic_account = self.project_id.create(vals)
            
            self.project_id = analytic_account.id

    # 6. CRUD methods
    # def create(self):


    # 7. Action methods
    # @api.multi
    # def action_validate(self):
    #     self.ensure_one()

    # 8. Business methods
    # def mail_user_confirm(self):
    