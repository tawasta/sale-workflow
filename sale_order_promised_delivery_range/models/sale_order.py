from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    date_delivery_promised_start = fields.Date(
        string="Promised Delivery start",
        readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
        copy=False,
    )

    date_delivery_promised_end = fields.Date(
        string="Promised Delivery end",
        readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
        copy=False,
    )

    @api.onchange("date_delivery_promised_start")
    def onchange_date_delivery_start_update_date_delivery_end(self):
        for record in self:
            start = record.date_delivery_promised_start or False
            end = record.date_delivery_promised_end

            if start:
                if not end or end < start:
                    record.date_delivery_promised_end = start

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        invoice_vals["date_delivery_promised_start"] = self.date_delivery_promised_start

        invoice_vals["date_delivery_promised_end"] = self.date_delivery_promised_end

        return invoice_vals
