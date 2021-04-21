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
        string="Check available",
        help="Do we need to check the availability of this line",
        compute="_compute_product_check_available",
    )

    product_virtual_available = fields.Float(
        string="Virtual available",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_product_virtual_available",
    )

    product_warehouse_available = fields.Float(
        string="Available",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_product_warehouse_available",
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
    def _compute_product_virtual_available(self):
        for record in self:
            record.product_virtual_available = record.product_id.virtual_available

    @api.onchange("product_uom_qty", "product_uom", "product_id")
    @api.depends("product_uom_qty", "product_uom", "product_id")
    def _compute_product_warehouse_available(self):
        Quant = self.env["stock.quant"]
        for record in self:
            # TODO: this will only check one sublevel
            warehouse = record.order_id.warehouse_id

            locations = (
                warehouse.lot_stock_id.ids
                + warehouse.lot_stock_id.child_ids.filtered(
                    lambda r: r.usage in ["internal", "transit"]
                ).ids
            )
            print(locations)

            domain = [
                ("product_id", "=", record.product_id.id),
                ("location_id", "in", locations),
            ]

            quants = Quant.search(domain)
            available = sum(quants.mapped("quantity")) - sum(
                quants.mapped("reserved_quantity")
            )
            record.product_warehouse_available = available

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
