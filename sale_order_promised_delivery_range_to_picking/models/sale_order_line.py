# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _action_procurement_create(self):
        procurements = super(SaleOrderLine, self)._action_procurement_create()

        StockPicking = self.env['stock.picking']
        for procurement in procurements:
            # Search all pickings in this procurement
            pickings = StockPicking.search([(
                ('group_id', '=', procurement.group_id.id)
            )])

            for picking in pickings:
                if self.order_id.date_delivery_promised_start:
                    picking.min_date = datetime.strptime(
                        self.order_id.date_delivery_promised_start,
                        DEFAULT_SERVER_DATE_FORMAT
                    ) \
                    + timedelta(days=self.customer_lead, hours=12)

                if self.order_id.date_delivery_promised_end:
                    picking.max_date = datetime.strptime(
                        self.order_id.date_delivery_promised_end,
                        DEFAULT_SERVER_DATE_FORMAT
                    ) \
                    + timedelta(days=self.customer_lead, hours=12)

        return procurements