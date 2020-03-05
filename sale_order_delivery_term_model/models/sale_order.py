from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    delivery_term_id = fields.Many2one(
        'delivery.term',
        string='Delivery Term',
    )
