# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    sale_order_count = fields.Integer(
        '# of Sales Order',
        compute='_sale_order_count'
    )
    invoices = fields.One2many(
        'account.invoice',
        'partner_id',
        string='Invoices',
        readonly=True
    )


    @api.one
    def _sale_order_count(self):

        child_ids = self._get_recursive_child_ids(self)
        child_ids.append(self.id)

        sale_orders = self.env['sale.order'].search([
            ('partner_id', 'in', child_ids)]
        )

        self.sale_order_count = len(sale_orders)
