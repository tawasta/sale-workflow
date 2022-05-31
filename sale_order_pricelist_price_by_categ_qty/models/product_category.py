from odoo import fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    use_on_discount = fields.Boolean(string="Use on Sale Order line discount",
        help=_("""Check this box to use this Product category on Sale Order
            line discount"""))
