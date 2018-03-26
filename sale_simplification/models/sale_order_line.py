# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import fields, models

# 4. Imports from Odoo modules (rarely, and only if necessary):

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrderLine(models.Model):
    # 1. Private attributes
    _inherit = 'sale.order.line'

    _FIELD_STATES = {
        'draft': [('readonly', False)],
        'confirmed': [('readonly', False)],
    }

    # 2. Fields declaration

    # Allow modifying fields until the invoice is created
    product_id = fields.Many2one(states=_FIELD_STATES)
    name = fields.Text(states=_FIELD_STATES)
    price_unit = fields.Float(states=_FIELD_STATES)
    tax_id = fields.Many2many(states=_FIELD_STATES)
    product_uom_qty = fields.Float(states=_FIELD_STATES)
    product_uom = fields.Many2one(states=_FIELD_STATES)
    product_uos_qty = fields.Float(states=_FIELD_STATES)
    product_uos = fields.Many2one(states=_FIELD_STATES)
    discount = fields.Float(states=_FIELD_STATES)
