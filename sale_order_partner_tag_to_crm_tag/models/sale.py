# 1. Standard library imports:
import logging

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import api, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges
    @api.onchange("partner_id")
    def _onchange_partner_id_tag_ids(self):
        if self.partner_id and self.partner_id.category_id:
            crm_tags = []
            for partner_tag in self.partner_id.category_id:
                if partner_tag.to_sale_order:
                    crm_tag = (
                        self.env["crm.tag"]
                        .sudo()
                        .search([("name", "=", partner_tag.name)], limit=1)
                    )
                    if not crm_tag:
                        crm_tag = (
                            self.env["crm.tag"]
                            .sudo()
                            .create({"name": partner_tag.name})
                        )
                        _logger.debug("Created a new CRM Tag %s" % crm_tag)
                    crm_tags.append((4, crm_tag.id, 0))
            self.update({"tag_ids": crm_tags})

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
