# -*- coding: utf-8 -*-
from openerp import models, api, fields
from openerp import exceptions
from openerp import _

import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    sale_order_lines = fields.One2many(
        'sale.order.line',
        'order_id',
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
    def write(self, vals):
        ''' Extends default write to update sale order as the
        opportunity progresses '''

        if 'stage_id' in vals:
            sale_action = self.stage_id.browse(vals['stage_id']).sale_action
            if sale_action:
                self._update_sale_order(sale_action)

        return super(CrmLead, self).write(vals)

    @api.one
    def _update_sale_order(self, sale_action):
        ''' Updates sale order on opportunity action stages '''
        if sale_action == 'quotation_send' and not self.sale_order:
            if not self.partner_id:
                warn = _("Please set a customer for the quotation") + " "
                warn += _("before moving it to this stage!")
                raise exceptions.Warning(warn)

            else:
                sale_order_object = self.env['sale.order']
                vals = {
                    'partner_id': self.partner_id.id,
                    'partner_invoice_id': self.partner_id.id,
                    'partner_shipping_id': self.partner_id.id,
                    'lead_id': self.id,
                }
                sale_order = sale_order_object.create(vals)
                self.sale_order = sale_order.id
                self.ref = sale_order

                msg = _("Sale order")
                msg += " <b>%s</b> " % self.sale_order.name
                msg += _("created")

                self.message_post(msg)

    def _get_sale_order_lines(self):
        for record in self:
            if record.sale_order:
                record.sale_order_lines = self.sale_order.order_line

    def _get_pricelist(self):
        for record in self:
            if record.sale_order:
                record.pricelist_id = record.sale_order.pricelist_id

    def _set_sale_order_lines(self):
        for record in self:
            if record.sale_order:
                record.sale_order.order_line = record.sale_order_lines
