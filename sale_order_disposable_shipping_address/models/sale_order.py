# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    partner_shipping_id_keep = fields.Boolean(
        string='Keep shipping address',
    )

    @api.multi
    def action_confirm(self):
        if not self.partner_shipping_id_keep:
            self.partner_shipping_id.active = False

        return super(SaleOrder, self).action_confirm()
