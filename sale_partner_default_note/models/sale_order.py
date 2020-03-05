# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges
    @api.onchange("partner_id")
    def onchange_partner_id_update_sale_note(self):
        for record in self:
            if record.partner_id and record.partner_id.sale_note:
                record.note = record.partner_id.sale_note

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
