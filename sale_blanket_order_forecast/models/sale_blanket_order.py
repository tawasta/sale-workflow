import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleBlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    create_forecast_sales = fields.Boolean(
        "Create forecast Sales",
        help="Select this if you want to create Sale orders that act as a forecast",
    )

    confirmed_sale_order_ids = fields.Many2many(
        string="Confirmed sales",
        comodel_name="sale.order",
        compute="_compute_confirmed_sale_order_ids",
    )

    confirmed_sale_order_ids_count = fields.Integer(
        string="Confirmed sales count", compute="_compute_confirmed_sale_order_ids"
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

    forecast_write_date = fields.Datetime(
        "Forecast updated",
        readonly=True,
        copy=False,
    )
    forecast_is_stale = fields.Boolean(
        "Forecast is stale",
        help="Forecast should be recomputed",
        compute="_compute_forecast_is_stale",
    )

    replacement_policy = fields.Selection(
        [
            ("none", "No replacing"),
            ("category", "Product category"),
        ],
        string="Replacement Policy",
        help="No replacing: Never replace exhausted product.\n"
        "Product category: After a product forecast is exhausted, "
        "use other products in the same category.\n",
        default="none",
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

    def _compute_confirmed_sale_order_ids(self):
        for record in self:

            if record.forecast_policy == "picking":
                # Search by picking date
                pickings = self.env["stock.picking"].search(
                    [
                        ("scheduled_date", ">=", self.validity_date_start),
                        ("scheduled_date", "<=", self.validity_date),
                        ("sale_id", "!=", False),
                        ("state", "not in", ["cancel"]),
                    ]
                )
                sale_orders = pickings.mapped("sale_id")
            else:
                # Search by SO date
                sale_orders = self.env["sale.order"].search(
                    [
                        ("date_order", ">=", self.validity_date_start),
                        ("date_order", "<=", self.validity_date),
                        ("is_forecast", "=", False),
                        ("state", "in", ["sale", "done"]),
                    ]
                )

            record.confirmed_sale_order_ids = sale_orders
            record.confirmed_sale_order_ids_count = len(sale_orders)

    def _compute_forecast_is_stale(self):
        for record in self:
            stale = False

            if not record.forecast_write_date:
                # Forecast has never been computed
                stale = True
            elif record.write_date > record.forecast_write_date:
                # Forecast is not computed after BO changes
                stale = True

            record.forecast_is_stale = stale

    @api.model
    def expire_orders(self):
        today = fields.Date.today()
        expired_orders = self.search(
            [
                ("state", "in", ["open", "done"]),
                ("validity_date", "<=", today),
            ]
        )

        for expired in expired_orders:
            if expired.forecast_sale_order_id.state in ["sale", "sent"]:
                expired.forecast_sale_order_id.action_cancel()

        return super().expire_orders()

    def cron_create_forecast(self):
        records = self.search([("state", "=", "open")])
        for record in records:
            record.action_create_forecast()

    def action_view_confirmed_sale_orders(self):
        sale_orders = self.confirmed_sale_order_ids
        action = self.env.ref("sale.action_orders").read()[0]
        if len(sale_orders) > 0:
            action["domain"] = [("id", "in", sale_orders.ids)]
            action["context"] = [("id", "in", sale_orders.ids)]
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    def action_create_forecast(self):
        self.ensure_one()
        if self.forecast_sale_order_id:
            sale_order = self.forecast_sale_order_id
        else:
            # Reset remaining qty to simulate a situation, where nothing is ordered yet
            for line in self.line_ids:
                line.remaining_uom_qty = line.original_uom_qty

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

        # Unlock locked sale
        if sale_order.state == "cancel":
            sale_order.action_draft()

        # Reopen cancelled sale
        if sale_order.state == "done":
            sale_order.action_unlock()

        # Return the SO to draft so it can be manipulated
        if sale_order.state == "sale":
            sale_order.action_cancel()
            sale_order.action_draft()

        # Set SO commitment date
        sale_order.commitment_date = self.validity_date_start

        # Tag the SO as BO forecast
        sale_order.is_forecast = True
        self.forecast_sale_order_id = sale_order.id

        # Recreate SO lines
        forecast_lines = self._compute_forecast_lines()
        for order_line in sale_order.order_line:
            product_id = order_line.product_id.id
            if forecast_lines.get(product_id) is not None:
                order_line.product_uom_qty = (
                    forecast_lines[product_id] if forecast_lines[product_id] > 0 else 0
                )

        # Confirm the SO to create deliveries
        sale_order.action_confirm()

        # Remove cancelled deliveries
        for picking in sale_order.picking_ids:
            if picking.state == "cancel":
                picking.unlink()

        # Unreserve products from pickings
        for picking in sale_order.picking_ids:
            picking.do_unreserve()

        # Update forecast date
        self.forecast_write_date = fields.Datetime.now()

        exhausted_lines = self.line_ids.filtered(
            lambda r: r.original_uom_qty <= r.realized_uom_qty
        )
        if exhausted_lines:
            msg = _(
                "Forecast computed. Exhausted products: {}".format(
                    ", ".join(exhausted_lines.mapped("product_id.name"))
                )
            )
            self.message_post(body=msg)

    def _compute_forecast_lines(self):
        # Compute forecast lines for the forecast SO

        # Sale Orders in the BO validity range
        sale_order_lines = self._get_confirmed_sale_order_lines()

        # Make a dict for products and fill it with "product_id: quantity"
        sold = self._get_sold_products(sale_order_lines)

        forecast_lines = {}
        for line in self.line_ids:
            product = line.product_id
            qty = line.original_uom_qty

            if sold.get(product.id):
                line.realized_uom_qty = sold[product.id]
                qty = qty - sold[product.id]

            if qty < 0:
                # Do a replacement for product that has been exhausted
                replacement_qty = abs(qty)
                if self.replacement_policy == "category":
                    replacement_lines = self.line_ids.filtered(
                        lambda r: r.product_id.categ_id == product.categ_id
                        and r.product_id != product
                    )
                    total = sum(replacement_lines.mapped("original_uom_qty"))
                    for rline in replacement_lines:
                        forecast_lines.setdefault(rline.product_id.id, 0)
                        forecast_lines[rline.product_id.id] -= (
                            rline.original_uom_qty / total * replacement_qty
                        )

                    qty = 0

            forecast_lines.setdefault(product.id, 0)
            forecast_lines[product.id] += qty

        return forecast_lines

    def _get_confirmed_sale_order_lines(self):
        sale_orders = self.confirmed_sale_order_ids

        _logger.info(
            _(
                f"Found {len(sale_orders)} sale orders "
                f"between {self.validity_date_start} and {self.validity_date}"
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
