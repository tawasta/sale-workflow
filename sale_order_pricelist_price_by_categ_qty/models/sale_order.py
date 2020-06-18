
from odoo import models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def compute_global_discount(self):
        """Button for calculating unit prices based on pricelist product quantities"""
        pricelist = self.pricelist_id
        # Create empty recordset for sale order line, this is used in dictionary
        sale_line_model = self.env['sale.order.line']
        categ_products = {}

        # First loop through sale order lines and fetch product categories and
        # sale order line records
        for line in self.order_line:
            product_category = line.product_id.categ_id
            if product_category:
                qty_and_line = categ_products.get(
                    product_category, [0, list(sale_line_model)]
                )
                # Result is a Python dictionary where keys are product categories
                # and values are sale order line records
                categ_products[product_category] = [
                    qty_and_line[0] + line.product_uom_qty, qty_and_line[1] + [line]
                ]

        # items are records within pricelist
        items = pricelist.mapped('item_ids')

        # Loop through product categories
        for categ in categ_products:
            # Loop through sale order line records
            for line in categ_products.get(categ)[1]:
                biggest_qty = max(items.mapped('min_quantity'))
                smallest_qty = 0
                index = 0
                item_price = 0
                # Keep looping until pricelist item with largest appropriate quantity
                # is fetched
                while smallest_qty < biggest_qty:
                    # Break the loop when all items have been checked
                    if index == len(items):
                        break
                    item = items[index]

                    prod_tmpl = item.product_tmpl_id

                    # Get item's price_surcharge-value only if
                    #     - Product template is used
                    #     - Quantitity used on item is equal or less than SO line qty
                    #     - Product template is the same as SO line's product template
                    if (prod_tmpl and prod_tmpl.categ_id == categ and
                            item.min_quantity <= categ_products.get(categ)[0] and
                            prod_tmpl == line.product_id.product_tmpl_id):
                        smallest_qty = item.min_quantity
                        # price_surcharge-field is item's added price and this is
                        # used to substitute sale order line's unit price
                        item_price = item.price_surcharge
                    index += 1
                if item_price:
                    line.price_unit = item_price
