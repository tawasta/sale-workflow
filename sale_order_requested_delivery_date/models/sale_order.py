from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_delivery_requested = fields.Datetime(
        string="Requested Delivery Date",
        help="Delivery date requested by the customer",
        copy=False,
    )
