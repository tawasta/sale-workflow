# -*- coding: utf-8 -*-
from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        # Add notice period to sale note
        for order in self:

            notice_period_days = self.partner_id.notice_period \
                or self.company_id.default_notice_period

            notice_period = _('Notice period: %s days') % notice_period_days

            if order.note:
                order.note = notice_period + '\n' + order.note

            else:
                order.note = notice_period

        return res
