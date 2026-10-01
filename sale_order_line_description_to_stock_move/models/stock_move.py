from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sale_line_id = vals.get("sale_line_id", False)

            sale_line = (
                self.env["sale.order.line"].sudo().search([("id", "=", sale_line_id)])
            )

            if sale_line:
                # Strip the product name from the description to avoid it showing
                # two times on the stock move
                description = sale_line.name.removeprefix(
                    sale_line.translated_product_name or ""
                ).strip()

                if description:
                    vals["description_picking"] = description

        return super().create(vals_list)
