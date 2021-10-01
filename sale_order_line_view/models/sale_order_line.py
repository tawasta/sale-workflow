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

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrderLine(models.Model):
    # 1. Private attributes
    _inherit = "sale.order.line"

    # 2. Fields declaration
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        related="order_id.partner_id",
        store=True,
        readonly=True,
    )

    destination_country_id = fields.Many2one(
        string="Destination",
        comodel_name="res.country",
        related="order_id.partner_shipping_id.country_id",
        store=True,
        readonly=True,
    )

    product_categ_id = fields.Many2one(
        string="Category",
        comodel_name="product.category",
        compute="_compute_product_categ_id",
        store=True,
        readonly=True,
    )

    date_order = fields.Datetime(
        string="Order date", related="order_id.date_order", store=True, readonly=True
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.onchange("product_id")
    @api.depends("product_id")
    def _compute_product_categ_id(self):
        for record in self:
            if record.product_id:
                record.product_categ_id = record.product_id.categ_id.id
            else:
                record.product_categ_id = False

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
