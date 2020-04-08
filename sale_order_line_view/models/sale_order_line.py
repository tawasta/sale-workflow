from odoo import models, fields


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    # Related/computed helper fields here
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        related="order_id.partner_id",
        store=True,
    )

    destination_country_id = fields.Many2one(
        string="Destination",
        comodel_name="res.country",
        related="order_id.partner_shipping_id.country_id",
        store=True,
    )

    product_categ_id = fields.Many2one(
        string="Category",
        comodel_name="product.category",
        related="product_id.categ_id",
        store=True,
    )

    date_order = fields.Datetime(
        string="Order date",
        related="order_id.date_order",
        store=True,
    )
