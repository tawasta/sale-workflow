# -*- coding: utf-8 -*-

from odoo import fields, models
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
            if record.amount_untaxed:
                margin_percent = (record.margin / record.amount_untaxed) * 100
                record.margin_percent = margin_percent
