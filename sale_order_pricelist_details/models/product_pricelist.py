# -*- coding: utf-8 -*-
from odoo import models, api


class ProductPricelist(models.Model):

    _inherit = 'product.pricelist'

    @api.multi
    def action_pricelist_line_tree(self):
        action = self.env.ref('sale_order_pricelist_details.action_pricelist_line_tree').read()[0]
        action['context'] = {
            'default_pricelist_id': self.id,
        }
        return action
