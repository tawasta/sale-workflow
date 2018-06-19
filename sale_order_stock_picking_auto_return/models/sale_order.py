# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    pickings_done = fields.Boolean(
        string='Sale has delivered pickings',
        compute='_compute_pickings_done',
    )

    def _compute_pickings_done(self):
        for record in self:
            record.pickings_done = \
                any([x.state == 'done' for x in record.picking_ids])
