from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def write(self, values):
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = self.tax_id.compute_all(
            price, self.order_id.currency_id, self.product_uom_qty,
            product=self.product_id, partner=self.order_id.partner_shipping_id)
        values['price_tax'] = sum(t.get('amount', 0.0) for t in
                                  taxes.get('taxes', []))
        values['price_total'] = taxes['total_included']
        values['price_subtotal'] = taxes['total_excluded']
        return super(SaleOrderLine, self).write(values)
