from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def print_quotation(self):
        # Remove the state-changing functionality from core's print button,
        # and just print the SO
        return self.env["report"].get_action(self, "sale.report_saleorder")

    def action_quotation_mark_sent(self):
        self.state = "sent"
