# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models, _
from openerp.exceptions import ValidationError

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):
    
    # 1. Private attributes
    _inherit = 'sale.order'

    # 2. Fields declaration
    order_line_without_tax_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        domain=[('tax_id', '=', False)],
    )
    bypass_mandatory_tax = fields.Boolean(
        string='Allow confirming without taxes',
        default=False,
        copy=False,
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_button_confirm(self):
        for record in self:
            if record.order_line_without_tax_ids and not record.bypass_mandatory_tax:
                raise ValidationError(_("Please set taxes for all the lines."))

        return super(SaleOrder, self).action_button_confirm()

    # 8. Business methods
