# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleReport(models.Model):

    _inherit = 'sale.report'

    partner_shipping_id = fields.Many2one(
        comodel_name='res.partner', string='Delivery Address',
        readonly=True)

    def _select(self):
        res = super(SaleReport, self)._select()
        return res + ', s.partner_shipping_id as partner_shipping_id'

    def _group_by(self):
        res = super(SaleReport, self)._group_by()
        return res + ', s.partner_shipping_id'
