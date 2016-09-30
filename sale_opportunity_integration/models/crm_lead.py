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

    sale_order_description = fields.Text(
        string='Description',
        compute='_get_sale_order_description',
        inverse='_set_sale_order_description',
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
        if (sale_action == 'quotation_send' or sale_action == 'opportunity_won')\
                and not self.sale_order:

            if not self.partner_id:
                warn = _("Please set a customer for the quotation") + " "
                warn += _("before moving it to this stage!")
                raise exceptions.Warning(warn)

            else:
                vals = {
                    'header_text': self.name,
                    'partner_id': self.partner_id.id,
                    'partner_invoice_id': self.partner_id.id,
                    'partner_shipping_id': self.partner_id.id,
                    'lead': self.id,
                    'description': self.description,
                }

                sale_order = self.sale_order.create(vals)
                self.sale_order = sale_order.id
                self.ref = sale_order

                msg = _("Sale order")
                msg += " <b>%s</b> " % self.sale_order.name
                msg += _("created")

                self.message_post(msg)

        elif (sale_action == 'opportunity_lost') and self.sale_order:
            self.sale_order.action_cancel()

            msg = _("Sale order")
            msg += " <b>%s</b> " % self.sale_order.name
            msg += _("cancelled")

            self.message_post(msg)

    @api.multi
    def _get_sale_order_lines(self):
        for record in self:
            if record.sale_order:
                record.sale_order_lines = record.sale_order.order_line

    @api.multi
    def _set_sale_order_lines(self):
        for record in self:
            if record.sale_order:
                record.sale_order.order_line = record.sale_order_lines

    @api.multi
    def _get_pricelist(self):
        for record in self:
            if record.sale_order:
                record.pricelist_id = record.sale_order.pricelist_id

    @api.multi
    def _get_sale_order_description(self):
        for record in self:
            if record.sale_order:
                record.sale_order_description = record.sale_order.description

    @api.multi
    def _set_sale_order_description(self):
        for record in self:
            if record.sale_order:
                record.sale_order.description = record.sale_order_description
                record.description = record.sale_order_description
