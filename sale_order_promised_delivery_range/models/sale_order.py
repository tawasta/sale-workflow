from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_delivery_promised_start = fields.Date(
        string="Promised Delivery Range (start)",
        copy=False,
    )

    date_delivery_promised_end = fields.Date(
        string="Promised Delivery Range (end)",
        copy=False,
    )

    @api.onchange("date_delivery_promised_start")
    def onchange_date_delivery_start_update_date_delivery_end(self):
        for record in self:
            start = record.date_delivery_promised_start or False
            end = record.date_delivery_promised_end or False

            if start and not end or end < start:
                record.date_delivery_promised_end = start
