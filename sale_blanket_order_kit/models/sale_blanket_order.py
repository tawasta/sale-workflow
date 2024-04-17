import logging

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleBlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    kit_ids = fields.One2many(
        "sale.blanket.order.kit",
        "order_id",
        string="Order Kits",
        copy=True,
    )

    kit_recompute_clear = fields.Boolean(
        "Clear lines on recompute",
        help="Clear all existing order lines on kit recompute",
        default=True,
    )

    # Allow disabling automated recompute for BO:s that are
    # modified manually
    kit_recompute_automatically = fields.Boolean(
        "Automatic kit recompute",
        help="Recompute order lines from kits automatically",
        default=True,
    )

    def cron_kit_recompute(self):
        records = self.search(
            [
                ("kit_recompute_automatically", "=", True),
            ]
        )
        for record in records:
            if record.kit_ids:
                # Only recompute if kits are set to prevent clearing other BO:s
                record.action_kit_compute()

    def action_kit_compute(self):
        for record in self:
            if record.kit_recompute_clear:
                record.line_ids.unlink()

            record._kit_expand()

            msg = _("Recomputed order lines based on the kits")
            self.message_post(body=msg)

    def _kit_expand(self):
        self.ensure_one()

        products = {}

        for kit_line in self.kit_ids:
            products = self._bom_lines_expand(
                kit_line.kit_id.bom_line_ids, products, kit_line.original_uom_qty
            )

        line_model = self.env["sale.blanket.order.line"]
        for product_id, qty in products.items():
            product = self.env["product.product"].browse([product_id])

            existing_line = line_model.search(
                [("order_id", "=", self.id), ("product_id", "=", product_id)], limit=1
            )

            if existing_line:
                existing_line.original_uom_qty = qty
            else:
                line_vals = {
                    "order_id": self.id,
                    "product_id": product_id,
                    "original_uom_qty": qty,
                    "product_uom": product.uom_id.id,
                    "price_unit": product.lst_price or 1,
                }
                line_model.create(line_vals)

    def _bom_lines_expand(self, bom_lines, products, quantity=1, recursive=True):
        for bom_line in bom_lines:
            converted_quantity = bom_line.product_uom_id._compute_quantity(
                quantity, bom_line.bom_id.product_uom_id
            )

            if (
                bom_line.child_bom_id
                and bom_line.child_bom_id.type == "phantom"
                and recursive
            ):
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
