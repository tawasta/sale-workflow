from odoo import fields
from odoo import models
from odoo import _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaleBlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    kit_ids = fields.One2many(
        "sale.blanket.order.kit",
        "order_id",
        string="Order Kits",
        copy=True,
    )

    def action_kit_compute(self):
        for record in self:
            record._kit_expand()

    def _kit_expand(self):
        self.ensure_one()

        products = {}
        for kit_line in self.kit_ids:
            products = self._bom_lines_expand(
                kit_line.kit_id.bom_line_ids, products, kit_line.original_uom_qty
            )

        self.line_ids = False

        for product_id, qty in products.items():
            product = self.env["product.product"].browse([product_id])
            line_vals = {
                "order_id": self.id,
                "product_id": product_id,
                "original_uom_qty": qty,
                "product_uom": product.uom_id.id,
                "price_unit": product.lst_price,
            }
            self.env["sale.blanket.order.line"].create(line_vals)

    def _bom_lines_expand(self, bom_lines, products, quantity=1):
        for bom_line in bom_lines:
            converted_quantity = bom_line.product_uom_id._compute_quantity(
                quantity, bom_line.bom_id.product_uom_id
            )

            if bom_line.child_bom_id:
                products = self._bom_lines_expand(
                    bom_line.child_line_ids,
                    products,
                    converted_quantity * bom_line.product_qty,
                )
            else:
                product = bom_line.product_id
                if product.uom_id != bom_line.product_uom_id:
                    raise ValidationError(_("Unit conversion is not yet supported"))
                products[product.id] = bom_line.product_qty * quantity + products.get(
                    product.id, 0
                )

        return products
