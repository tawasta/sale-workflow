from datetime import datetime
from odoo import models
from timeit import default_timer as timer_ticker
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def compute_global_discount(self):
        """
        Button for calculating unit prices based on pricelist product quantities
        """
        start = timer_ticker()
        pricelist = self.pricelist_id
        # Create empty recordset for sale order line to be used in a dictionary
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
                # Result is a Python dictionary where keys are product
                # categories and values are sale order line records.
                # Also sums all the product quantities that belong to the same
                # product category. This value is used when comparing
                # pricelist's items
                categ_products[product_category] = [
                    qty_and_line[0] + line.product_uom_qty,
                    qty_and_line[1] + [line]
                ]

        date_now = datetime.now().date()

        # Loop through product categories
        for categ in categ_products:
            # Loop through sale order line records
            for line in categ_products.get(categ)[1]:
                # Variable 'items' are lines within pricelist.
                # This might look messy but all we are doing here, is sort the
                # records by min_quantity (from smallest to largest) and filter
                # out those records that do not belong to the same category as
                # sale order line's product. Filtering is not necessary, code
                # just runs faster with it
                items = pricelist.mapped('item_ids').sorted(
                    key=lambda t: t.min_quantity).filtered(
                    lambda x: x.product_tmpl_id and
                        x.product_tmpl_id.categ_id.id ==
                        line.product_id.categ_id.id)
                if not items:
                    continue

                biggest_qty = max(items.mapped('min_quantity'))
                smallest_qty = 0
                index = 0
                item_price = 0
                # Keep looping until pricelist item with largest appropriate
                # quantity is fetched
                while smallest_qty < biggest_qty:
                    # Break the loop when all items have been checked
                    if index == len(items):
                        break
                    item = items[index]

                    # Only use items whose time period has not ended and if item has
                    # a starting date, then it needs to be earlier than current date
                    if ((item.date_end and (date_now - item.date_end).days > 0)
                            or (item.date_start
                                and (date_now - item.date_start).days < 0)):
                        index += 1
                        continue

                    prod_tmpl = item.product_tmpl_id

                    # Get item's price_surcharge-value only if:
                    # Product template is used and product has the same category
                    # as sale order line's product's category
                    # Quantity used on item is equal or less than SO line qty
                    # Product template is the same as SO line's product template
                    if (prod_tmpl and prod_tmpl.categ_id == categ and
                            item.min_quantity <= categ_products.get(categ)[0]
                            and prod_tmpl == line.product_id.product_tmpl_id):
                        smallest_qty = item.min_quantity
                        # price_surcharge-field is item's added price and
                        # it is used to substitute sale order line's unit price
                        item_price = item.price_surcharge

                        # Add attribute extra to pricelist price
                        if item.applied_on != '0_product_variant':
                            item_price += line.product_id.price_extra
                    index += 1
                if item_price:
                    line.price_unit = item_price

        end = timer_ticker()
        time_spent = end - start
        # Time taken is useful to know if SO and/or pricelist has many lines
        _logger.info("Time spent on Compute global discount-method: %ss"
                     % time_spent)
