from odoo import models

# Line fields priced for a unit. sale_attached_product prices the attached line in
# the product's base unit, so these are left for create to compute in the new unit.
UNIT_PRICE_FIELDS = (
    "price_unit",
    "technical_price_unit",
    "discount",
    "pricelist_item_id",
)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_attached_line_values_product(self, line, product):
        """Give the attached line the main line's unit when the product allows it."""
        # Values prepared in the product's base unit, priced for one base unit
        vals = super()._get_attached_line_values_product(line, product)
        uom = line._get_attached_line_uom(product)
        if vals.get("product_uom_id") != uom.id:
            vals["product_uom_id"] = uom.id
            # Drop the base unit prices: create computes them for the new unit
            for field_name in UNIT_PRICE_FIELDS:
                vals.pop(field_name, None)
        # The quantity stays the main line's number, e.g. 1 × 6-pack main
        # product -> 1 × 6-pack attached product
        return vals

    def _update_attached_lines(self):
        """Make the attached lines follow a main line unit change. Runs only on
        quotations, as sale_attached_product syncs only those."""
        res = super()._update_attached_lines()
        for attached_line in self.order_line.attached_line_ids:
            main_line = attached_line.attached_from_line_id
            uom = main_line._get_attached_line_uom(attached_line.product_id)
            if attached_line.product_uom_id != uom:
                attached_line.with_context(
                    skip_auto_refresh_attached_product=True
                ).write({"product_uom_id": uom.id})
        return res
