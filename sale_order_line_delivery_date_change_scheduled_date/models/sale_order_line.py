from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    line_delivery_date = fields.Datetime(string="Delivery Date")

    @api.depends(
        "product_id",
        "customer_lead",
        "product_uom_qty",
        "product_uom",
        "order_id.commitment_date",
        "move_ids",
        "move_ids.forecast_expected_date",
        "move_ids.forecast_availability",
        "line_delivery_date",
    )
    def _compute_qty_at_date(self):
        res = super()._compute_qty_at_date()
        for line in self:
            if line.line_delivery_date:
                line.scheduled_date = line.line_delivery_date

        return res

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        invoice_line_vals = super()._prepare_invoice_line(**optional_values)

        if self.line_delivery_date:
            invoice_line_vals["line_delivery_date"] = self.line_delivery_date

        return invoice_line_vals
