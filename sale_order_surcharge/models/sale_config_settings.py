# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleConfigSettings(models.TransientModel):

    _inherit = 'sale.config.settings'

    surcharge_product_id = fields.Many2one(
        related='company_id.surcharge_product_id',
        string='Surcharge Product',
        domain=[('type', '=', 'service')],
    )

    surcharge_percentage = fields.Float(
        related='company_id.surcharge_percentage',
        string='Surcharge Percentage'
    )
