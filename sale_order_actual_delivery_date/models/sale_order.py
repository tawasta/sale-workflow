from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.depends("order_line.qty_delivered")
    def _compute_date_delivery_actual(self):
        for order in self:
            # The order contains physical products all of which have been
            # delivered
            if all(
                [
                    l.qty_delivered >= l.product_uom_qty
                    for l in order.order_line
                    if l.product_id.type != "service"
                ]
            ) and any([l.product_id.type != "service" for l in order.order_line]):

                order.date_delivery_actual = fields.Datetime.now()

    date_delivery_actual = fields.Datetime(
        compute="_compute_date_delivery_actual",
        string="Actual Delivery Date",
        readonly=True,
        store=True,
        help="Date of shipping out all the ordered products",
    )
