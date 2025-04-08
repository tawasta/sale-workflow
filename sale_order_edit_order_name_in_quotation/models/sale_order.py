from odoo import api, exceptions, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("name")
    def search_duplicate_sale_order_name(self):
        duplicate_sale_name = self.env["sale.order"].search([("name", "=", self.name)])

        if duplicate_sale_name:
            msg = (
                "A sale order %s already exists with this name.\n"
                "Please choose another name."
            ) % self.name
            raise exceptions.UserError(msg)
