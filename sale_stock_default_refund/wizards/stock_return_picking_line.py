# -*- coding: utf-8 -*-
from odoo import models, fields


class StockReturnPickingLine(models.TransientModel):

    _inherit = "stock.return.picking.line"

    to_refund_so = fields.Boolean(
        default=True,
    )
