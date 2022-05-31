from odoo import fields, models


class sale_order_inherit(models.Model):
    _inherit = 'sale.order'

    def _default_sale_type(self):
        return self.env['sale.type'].search([
            (
                'code',
                '=',
                'regular'
            )
        ]).id

    sale_type = fields.Many2one(
        comodel_name="sale.type",
        default=_default_sale_type,
    )
