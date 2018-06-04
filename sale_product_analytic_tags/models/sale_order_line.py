# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def onchange_product_id_update_analytic_tags(self):
        for record in self:
            if record.product_id and record.product_id.get_analytic_tags():
                record.analytic_tag_ids += \
                    record.product_id.get_analytic_tags()