# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

class SaleOrder(models.Model):
    
    # 1. Private attributes
    _inherit = 'sale.order'

    _FIELD_STATES = {
        'draft': [('readonly', False)],
        'sent': [('readonly', False)],
        'manual': [('readonly', False)],
    }

    # 2. Fields declaration
    ## Allow modifying fields until the invoice is created

    ### Partner
    partner_id = fields.Many2one(states=_FIELD_STATES)
    partner_invoice_id = fields.Many2one(states=_FIELD_STATES)
    partner_shipping_id = fields.Many2one(states=_FIELD_STATES)
    customer_contact = fields.Many2one(states=_FIELD_STATES, readonly=True)

    ### Order
    date_order = fields.Datetime(states=_FIELD_STATES)
    order_line = fields.One2many(states=_FIELD_STATES)
    header_text = fields.Char(states=_FIELD_STATES, readonly=True)
    client_order_ref = fields.Char(string='Reference', states=_FIELD_STATES, readonly=True)
    user_id = fields.Many2one(states=_FIELD_STATES, readonly=True)
    origin = fields.Char(states=_FIELD_STATES, readonly=True)

    ### Stock
    warehouse_id = fields.Many2one(states=_FIELD_STATES, readonly=True)

    ### Accounting
    payment_term = fields.Many2one(states=_FIELD_STATES, readonly=True)
    incoterm = fields.Many2one(states=_FIELD_STATES, readonly=True)
    fiscal_position = fields.Many2one(states=_FIELD_STATES, readonly=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
