# -*- coding: utf-8 -*-
from odoo import api, models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.depends('order_line.qty_delivered')
    def _compute_date_delivery_actual(self):
        for order in self:
            # All physical products have been delivered
            # and the field has not been previously set
            if all([l.qty_delivered >= l.product_uom_qty for l
                    in order.order_line
                    if l.product_id.type != 'service']) and \
                    not order.date_delivery_actual:

                order.date_delivery_actual = fields.Datetime.now()

    date_delivery_actual = fields.Date(
        compute='_compute_date_delivery_actual',
        string='Actual Delivery Date',
        readonly=True,
        store=True,
        help='Date of delivering all the ordered products shipped'
    )
