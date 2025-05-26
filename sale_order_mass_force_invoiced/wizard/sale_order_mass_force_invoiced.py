from odoo import _, exceptions, fields, models


class SaleOrderMassForceInvoiced(models.TransientModel):
    _name = "sale.order.mass.force.invoiced"
    _description = "Sale order – Force Invoiced en mass"

    order_ids = fields.Many2many(
        "sale.order", default=lambda self: self._default_sale_orders()
    )

    def _default_sale_orders(self):
        return self.env["sale.order"].browse(self._context.get("active_ids"))

    def force_invoiced(self):
        sale_orders = self.env["sale.order"].browse(self._context.get("active_ids"))

        if any(sale.state != "sale" for sale in sale_orders):
            msg = _("Please select only confirmed sale orders")
            raise exceptions.UserError(msg)

        for sale_order in sale_orders:
            sale_order.write({"force_invoiced": True})
