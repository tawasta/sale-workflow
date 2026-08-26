from odoo import fields, models


class SaleOrderKioskMessage(models.TransientModel):
    _name = "sale.order.kiosk.message"
    _description = "Sale Kiosk - message"

    message = fields.Text()

    def action_close(self):
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
