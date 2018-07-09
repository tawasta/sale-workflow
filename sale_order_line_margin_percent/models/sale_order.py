# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    margin_percent = fields.Float(
        string='Margin (%)',
        digits=dp.get_precision('Margin'),
        compute='_compute_margin_percent',
    )

    def _compute_margin_percent(self):
        for record in self:
            line_sum = sum(record.order_line.filtered(
                lambda r: r.state != 'cancel').mapped('price_subtotal'))
            line_margin = sum(record.order_line.filtered(
                lambda r: r.state != 'cancel').mapped('margin'))

            record.margin_percent = round(line_margin / line_sum, 4) * 100
