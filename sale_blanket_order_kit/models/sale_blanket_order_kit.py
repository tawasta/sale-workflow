from odoo import api, fields, models


class SaleBlanketOrderKit(models.Model):
    _name = "sale.blanket.order.kit"

    order_id = fields.Many2one("sale.blanket.order", required=True, ondelete="cascade")

    kit_id = fields.Many2one(
        comodel_name="mrp.bom",
        name="Kit",
        domain=[("type", "=", "phantom")],
        required=True,
    )

    original_uom_qty = fields.Float(
        "Original quantity",
        required=True,
        default=1,
        digits="Product Unit of Measure",
    )

    @api.model
    def create(self, values):
        res = super().create(values)

        orders = res.mapped("order_id")
        orders.action_kit_compute()

        return res

    def write(self, values):
        res = super().write(values)

        orders = self.mapped("order_id")
        orders.action_kit_compute()

        return res

    def unlink(self):
        orders = self.mapped("order_id")
        res = super().unlink()

        orders.action_kit_compute()

        return res
