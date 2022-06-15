import logging

from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleBlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    create_forecast_sales = fields.Boolean(
        "Create forecast Sales",
        help="Select this if you want to create Sale orders that act as a forecast",
    )

    forecast_policy = fields.Selection(
        [
            ("order", "Ordered quantities"),
            ("delivery", "Delivered quantities"),
            ("picking", "Picking"),
        ],
        string="Forecast Policy",
        help="Ordered Quantity: Forecast using ordered quantities.\n"
        "Delivered Quantity: Forecast using delivered quantities.\n"
        "Picking: Forecast using quantities on pickings (Kits are expanded).\n",
        default="order",
    )

    forecast_sale_order_id = fields.Many2one(
        comodel_name="sale.order", string="Forecast sale", readonly=1, copy=False
    )

    validity_date = fields.Date(string="Validity end")

    validity_date_start = fields.Date(
        "Validity start",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    def action_create_forecast(self):
        if self.forecast_sale_order_id:
            sale_order = self.forecast_sale_order_id
        else:
            # Create a new SO
            bo_values = {}
            bo_wizard = (
                self.env["sale.blanket.order.wizard"]
                .with_context(
                    {
                        "active_ids": [self.id],
                        "active_id": self.id,
                        "active_model": "sale.blanket.order",
                    }
                )
                .create(bo_values)
            )

            # Wizard values can be manipulated here

            sale_order_id = bo_wizard.create_sale_order().get("domain")[0][2][0]
            sale_order = self.env["sale.order"].browse([sale_order_id])

        # Return the SO to draft so it can be manipulated
        if sale_order.state == "sale":
            sale_order.action_cancel()
            sale_order.action_draft()

        # Tag the SO as BO forecast
        sale_order.is_forecast = True
        self.forecast_sale_order_id = sale_order.id

        # Recreate SO lines
        forecast_lines = self._compute_forecast_lines()
        for order_line in sale_order.order_line:
            product_id = order_line.product_id.id
            if forecast_lines.get(product_id):
                order_line.product_uom_qty = (
                    forecast_lines[product_id] if forecast_lines[product_id] > 0 else 0
                )

        # Confirm the SO to create deliveries
        sale_order.action_confirm()

    def _compute_forecast_lines(self):
        # Compute forecast lines for the forecast SO

        # Sale Orders in the BO validity range
        sale_order_lines = self._get_confirmed_sale_order_lines()

        # Make a dict for products and fill it with "product_id: quantity"
        sold = self._get_sold_products(sale_order_lines)

        forecast_lines = {}
        for forecast in self.line_ids:
            product = forecast.product_id
            qty = forecast.original_uom_qty

            if sold.get(product.id):
                qty = qty - sold[product.id]

            forecast_lines[product.id] = qty

        return forecast_lines

    def _get_confirmed_sale_order_lines(self):
        sale_orders = self.env["sale.order"].search(
            [
                ("date_order", ">=", self.validity_date_start),
                ("date_order", "<=", self.validity_date),
                ("is_forecast", "=", False),
                ("state", "in", ["sale", "done"]),
            ]
        )

        _logger.info(
            _(
                "Found {} sale orders between {self.validity_date_start} and {}".format(len(sale_orders), self.validity_date)
            )
        )

        lines = sale_orders.mapped("order_line")

        return lines

    def _get_sold_products(self, sale_order_lines):
        sold = {}

        for line in sale_order_lines:
            # Loop each line as we need to check for kit products
            if self.forecast_policy == "order":
                product = line.product_id
                qty = line.product_uom_qty

                sold.update({product.id: sold.get(product.id, 0) + qty})
            elif self.forecast_policy == "delivery":
                product = line.product_id
                qty = line.qty_delivered

                sold.update({product.id: sold.get(product.id, 0) + qty})
            elif self.forecast_policy == "picking":
                for move in line.move_ids:
                    if move.state == "cancel":
                        continue
                    product = move.product_id
                    qty = move.product_uom_qty

                    sold.update({product.id: sold.get(product.id, 0) + qty})
            else:
                raise ValidationError(_("Please select a forecast policy"))

        return sold
