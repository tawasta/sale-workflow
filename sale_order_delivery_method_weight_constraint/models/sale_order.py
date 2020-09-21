from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    total_delivery_weight = fields.Float(
        compute="_compute_total_delivery_weight")
    max_weight = fields.Float(related="carrier_id.max_weight")
    min_weight = fields.Float(related="carrier_id.min_weight")

    # Trigger computation if SO line's Quantity, Product
    # or Delivery method changes
    @api.depends('order_line.product_uom_qty', 'order_line.product_id',
                 'carrier_id')
    def _compute_total_delivery_weight(self):
        """Compute Total delivery weight and compare the computed value to
        Delivery method's maximum and minimum weights"""
        for sale in self:
            sale.total_delivery_weight = sum(
                [x.product_id.weight * x.product_uom_qty for
                 x in sale.order_line])
            # Remove Delivery Method if summed products' weight is more than
            # Delivery Method's maximum weight or summed products' weight is
            # less than Delivery Method's minimum weight. Also check if Delivery
            # Method has assigned maximum or minimum weight.
            if ((sale.carrier_id.max_weight and
                 sale.carrier_id.max_weight < sale.total_delivery_weight) or
                (sale.carrier_id.min_weight and
                 sale.carrier_id.min_weight > sale.total_delivery_weight)):
                sale.carrier_id = None
