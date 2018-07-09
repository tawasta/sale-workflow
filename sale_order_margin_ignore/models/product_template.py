# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    margin_ignore = fields.Boolean(
        string='Ignore in margin',
        help='Ignore this product when computing margins',
        default=False,
    )
