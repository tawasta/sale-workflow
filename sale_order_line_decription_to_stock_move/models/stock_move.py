from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, vals):
        sale_line_id = vals.get("sale_line_id", False)

        sale_line = (
            self.env["sale.order.line"].sudo().search([("id", "=", sale_line_id)])
        )

        if sale_line:
            vals["description_picking"] = sale_line.name

        return super().create(vals)
