from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    in_finalization = fields.Boolean(
        string='In finalization',
    )
