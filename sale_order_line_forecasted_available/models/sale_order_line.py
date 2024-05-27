from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    virtual_available = fields.Float(
        "Forecast Quantity", compute="_compute_forecast_value", store=True
    )

    @api.depends("product_id")
    def _compute_forecast_value(self):
        for rec in self:
            if (
                rec.product_id
                and rec.product_id.product_tmpl_id
                and rec.product_id.product_tmpl_id.virtual_available
            ):
                rec.virtual_available = rec.product_id.product_tmpl_id.virtual_available
