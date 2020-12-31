from odoo import api
from odoo import fields
from odoo import models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    # Related/computed helper fields here
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        related="order_id.partner_id",
        store=True,
        readonly=True,
    )

    destination_country_id = fields.Many2one(
        string="Destination",
        comodel_name="res.country",
        related="order_id.partner_shipping_id.country_id",
        store=True,
        readonly=True,
    )

    product_categ_id = fields.Many2one(
        string="Category",
        comodel_name="product.category",
        compute="_compute_product_categ_id",
        store=True,
        readonly=True,
    )

    date_order = fields.Datetime(
        string="Order date", related="order_id.date_order", store=True, readonly=True,
    )

    @api.onchange("product_id")
    @api.depends("product_id")
    def _compute_product_categ_id(self):
        for record in self:
            if record.product_id:
                record.product_categ_id = record.product_id.categ_id.id
            else:
                record.product_categ_id = False
