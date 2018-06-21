# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    @api.model
    def default_get(self, fields):
        # Force to_refund_so as True

        res = super(StockReturnPicking, self).default_get(fields)
        i = 0
        for move in res.get('product_return_moves'):
            try:
                res['product_return_moves'][i][2]['to_refund_so'] = True
                i += 1
            except IndexError:
                pass

        return res
