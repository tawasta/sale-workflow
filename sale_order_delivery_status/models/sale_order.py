from odoo import fields, models


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields
    delivery_status = fields.Selection(
        selection=[
            ("none", "Nothing to Deliver"),
            ("open", "To Deliver"),
            ("partial", "Partially Delivered"),
            ("done", "Fully Delivered"),
        ],
        compute="_compute_delivery_status",
        string="Delivery Status",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_delivery_status(self):
        """Calculates the order's delivery status by comparing the lines'
        delivered quantities to ordered quantities. Service lines are ignored
        in the calculation"""

        for order in self:
            if all(
                [
                    l.product_id.type == "service" or l.product_uom_qty == 0
                    for l in order.order_line
                ]
            ):
                # All services or lines with 0 qties, nothing to deliver
                order.delivery_status = "none"
            elif all(
                [
                    l.qty_delivered >= l.product_uom_qty
                    for l in order.order_line
                    if l.product_id.type != "service"
                ]
            ):
                # All physical products have been delivered
                order.delivery_status = "done"
            elif all(
                [
                    l.qty_delivered == 0
                    for l in order.order_line
                    if l.product_id.type != "service"
                ]
            ):
                # No physical products have been delivered
                order.delivery_status = "open"
            else:
                # Some physical products have been delivered
                order.delivery_status = "partial"

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
