from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def create(self, vals):
        res = super().create(vals)

        product_pricelist = res.product_id and res.product_id.pricelist_id
        # grant_pricelist = product_pricelist and res.order_id.pricelist_id != product_pricelist
        # Granting a pricelist is disabled, as it would allow getting all items with the selected pricelist
        grant_pricelist = False

        if grant_pricelist:
            # Product adds a pricelist, but it hasn't been added yet
            res.order_id.pricelist_id = product_pricelist

        return res

    def _compute_pricelist_item_id(self):
        res = super()._compute_pricelist_item_id()

        # Check if products are adding a pricelist
        product_pricelists = self.mapped("product_id.pricelist_id")

        # TODO: if multiple pricelists are found, which is used?
        pricelist_id = product_pricelists[0] if product_pricelists else False

        first_line = self.order_id.order_line and self.order_id.order_line[0]
        for line in self:
            if first_line and line != first_line and pricelist_id:
                if pricelist_id == line.order_id.pricelist_id:
                    # If order is already using this pricelist, do nothing
                    continue
                # If products in order add a pricelist, use that for subsequent lines
                line.pricelist_item_id = pricelist_id._get_product_rule(
                    line.product_id,
                    quantity=line.product_uom_qty or 1.0,
                    uom=line.product_uom,
                    date=line.order_id.date_order,
                )

        return res
