from odoo import models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_launch_stock_rules(self):
        for record in self:
            for line in record.order_line:
                line._action_launch_stock_rule()
