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
        # Computes margin percent from SO lines

        # If sale_order_margin_ignore is in use
        margin_ignore = hasattr(self.env['product.template'], 'margin_ignore')

        for record in self:
            if record.amount_untaxed:
                amount_untaxed = record.amount_untaxed

                if margin_ignore:
                    # Subtract ignored lines from margin percent
                    for line in record.order_line.filtered(
                            lambda l: l.product_id.margin_ignore):
                        amount_untaxed -= line.price_subtotal

                margin_percent = (record.margin / amount_untaxed) * 100
                record.margin_percent = margin_percent
