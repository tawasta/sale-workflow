# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo import _

import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    order_line_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string='Order Lines',
        compute='_get_sale_order_lines',
        inverse='_set_sale_order_lines',
    )

    pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Pricelist',
        compute='_get_pricelist',
    )

    @api.multi
    def action_set_lost(self):
        for record in self:
            for order in record.order_ids:
                if order.state in ['draft', 'sent']:
                    order.message_post(_('Opportunity lost'))
                    order.action_cancel()

        return super(CrmLead, self).action_set_lost()

    @api.multi
    def action_set_won(self):
        for record in self:
            for order in record.order_ids:
                if order.state in ['draft', 'sent']:
                    order.message_post(_('Opportunity won'))
                    order.action_confirm()

        return super(CrmLead, self).action_set_won()

    @api.multi
    def _get_sale_order_lines(self):
        for record in self:
            if record.sale_number == 1:
                record.order_line_ids = record.order_ids\
                    .filtered(lambda r: r.state in ('draft', 'sent'))\
                    .order_line

    @api.multi
    def _set_sale_order_lines(self):
        for record in self:
            if record.sale_number == 1:
                record.order_ids \
                    .filtered(lambda r: r.state in ('draft', 'sent'))\
                    .order_line = record.order_line_ids

    @api.multi
    def _get_pricelist(self):
        for record in self:
            if record.sale_number == 1:
                record.pricelist_id = record.order_ids \
                    .filtered(lambda r: r.state in ('draft', 'sent'))\
                    .pricelist_id
