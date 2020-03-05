from datetime import datetime, timedelta

from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.multi
    def _action_procurement_create(self):
        procurements = super(SaleOrderLine, self)._action_procurement_create()

        StockPicking = self.env["stock.picking"]
        sale_order = self[0].order_id

        for procurement in procurements:
            # Search all pickings in this procurement
            pickings = StockPicking.search(
                [(("group_id", "=", procurement.group_id.id))]
            )

            for picking in pickings:
                if sale_order.date_delivery_promised_start:
                    picking.min_date = datetime.strptime(
                        sale_order.date_delivery_promised_start,
                        DEFAULT_SERVER_DATE_FORMAT,
                    ) + timedelta(days=self[0].customer_lead, hours=20)

                if sale_order.date_delivery_promised_end:
                    picking.max_date = datetime.strptime(
                        sale_order.date_delivery_promised_end,
                        DEFAULT_SERVER_DATE_FORMAT,
                    ) + timedelta(days=self[0].customer_lead, hours=20)

        return procurements
