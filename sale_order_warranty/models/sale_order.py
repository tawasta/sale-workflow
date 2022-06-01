from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    warranty = fields.Text(
        string='Warranty',
    )
