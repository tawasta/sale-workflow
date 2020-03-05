from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    date_delivery_promised = fields.Datetime(
        string="Promised Delivery Date",
        readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
        copy=False,
    )
