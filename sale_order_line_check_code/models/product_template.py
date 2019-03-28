# -*- coding: utf-8 -*-


from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    additional_code = fields.Boolean(string="Custom product", default=False)
    