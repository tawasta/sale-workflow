# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        # Add notice period to sale note
        for order in self:

            notice_period = _('Notice period: %s days') % \
                            self.partner_id.notice_period \
                            or self.company_id.default_notice_period

            if order.note:
                order.note += '\n' + notice_period
            else:
                order.note = notice_period

        return res
