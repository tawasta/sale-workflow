from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_forecast = fields.Boolean(related="sale_id.is_forecast")

    def remove_picking(self):
        # Helper for delayed jobs
        self.unlink()
