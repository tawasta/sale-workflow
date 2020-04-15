from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    delivery_place = fields.Char(string="Delivery Place")
