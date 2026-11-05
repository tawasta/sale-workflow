from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # Related (not stored): the list view needs a field on the line itself,
    # and image_128 already falls back to the template image on the variant.
    product_image = fields.Image(
        string="Image",
        related="product_id.image_128",
        readonly=True,
    )
