from odoo import fields, models


class BlanketOrderLine(models.Model):
    _inherit = "sale.blanket.order.line"

    realized_uom_qty = fields.Float(
        string="Realized qty", help="Realized quantity for forecast"
    )

    create_forecast_sales = fields.Boolean(related="order_id.create_forecast_sales")
