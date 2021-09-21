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
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrder(models.Model):
    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields declaration
    delivery_status = fields.Selection(
        selection=[
            ("none", "Nothing to Deliver"),
            ("open", "To Deliver"),
            ("partial", "Partially Delivered"),
            ("done", "Fully Delivered"),
        ],
        compute="_compute_delivery_status",
        string="Delivery Status",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_delivery_status(self):
        """Calculates the order's delivery status by comparing the lines'
        delivered quantities to ordered quantities. Service lines are ignored
        in the calculation"""

        for order in self:
            if all(
                [
                    l.product_id.type == "service" or l.product_uom_qty == 0
                    for l in order.order_line
                ]
            ):
                # All services or lines with 0 qties, nothing to deliver
                order.delivery_status = "none"
            elif all(
                [
                    l.qty_delivered >= l.product_uom_qty
                    for l in order.order_line
                    if l.product_id.type != "service"
                ]
            ):
                # All physical products have been delivered
                order.delivery_status = "done"
            elif all(
                [
                    l.qty_delivered == 0
                    for l in order.order_line
                    if l.product_id.type != "service"
                ]
            ):
                # No physical products have been delivered
                order.delivery_status = "open"
            else:
                # Some physical products have been delivered
                order.delivery_status = "partial"

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methodsfrom odoo import fields, models
