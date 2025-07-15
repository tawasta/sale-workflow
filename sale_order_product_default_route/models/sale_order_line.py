
from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    def write(self, values):
        res = super().write(values)

        product_id = values.get('product_id', False)
        if product_id:
            product = self.env['product.product'].browse(product_id)
            route_id = product.route_ids.filtered(lambda x: x.use_on_sale_line)

            if route_id:
                values['route_id'] = route_id.id
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            product_id = values.get('product_id', False)
            if product_id:
                product = self.env['product.product'].browse(product_id)
                route_id = product.route_ids.filtered(lambda x: x.use_on_sale_line)

                if route_id:
                    values['route_id'] = route_id.id
        return super(SaleOrderLine, self).create(vals_list)
