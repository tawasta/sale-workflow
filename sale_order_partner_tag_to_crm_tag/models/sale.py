##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

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
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
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
        return res

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
