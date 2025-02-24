##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models

from odoo.addons import decimal_precision as dp

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrderLine(models.Model):
    # 1. Private attributes
    _inherit = "sale.order.line"

    # 2. Fields declaration
    check_available = fields.Boolean(
        string="Check unreserved available",
        help="Do we need to check the availability of this line",
        compute="_compute_product_check_available",
    )

    product_qty_available_unreserved = fields.Float(
        string="Unreserved Available",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_product_qty_available_unreserved",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.onchange("product_id")
    @api.depends("product_id")
    def _compute_product_check_available(self):
        for record in self:
            order_open = record.state in ("draft", "sent")
            product_stockable = record.product_id.type == "product"

            record.check_available = order_open and product_stockable

    @api.onchange("product_uom_qty", "product_uom", "product_id")
    @api.depends("product_uom_qty", "product_uom", "product_id")
    def _compute_product_qty_available_unreserved(self):
        for record in self:
            record.product_qty_available_unreserved = (
                record.product_id.qty_available_unreserved
            )

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
