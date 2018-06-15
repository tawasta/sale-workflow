# -*- coding: utf-8 -*-
from odoo import api, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.onchange('type')
    def _onchange_type(self):
        super(ProductTemplate, self)._onchange_type()
        self.track_service = 'manual'
