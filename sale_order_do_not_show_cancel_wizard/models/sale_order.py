from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _show_cancel_wizard(self):
        return False
