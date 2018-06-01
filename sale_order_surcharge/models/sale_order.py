# -*- coding: utf-8 -*-
from odoo import models, fields, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def action_confirm(self):
        # Add a new order line with the surcharge, if necessary
        if self.partner_id.apply_surcharge \
                and self.company_id.surcharge_product_id \
                and self.company_id.surcharge_percentage:

            surcharge_amount = self.amount_untaxed \
                * (self.company_id.surcharge_percentage / 100)

            self.env['sale.order.line'].create({
                'order_id': self.id,
                'product_id': self.company_id.surcharge_product_id.id,
                'product_uom_qty': 1,
                'price_unit': surcharge_amount
            })

        return super(SaleOrder, self).action_confirm()

    def _compute_surcharge_note(self):
        # Show an informative note indicating that a surcharge will be added
        for sale in self:
            if sale.partner_id.apply_surcharge \
                    and sale.company_id.surcharge_product_id \
                    and sale.company_id.surcharge_percentage:

                note = _('%s (%s %%) will be added upon order confirmation') \
                    % (sale.company_id.surcharge_product_id.name,
                       sale.company_id.surcharge_percentage)
                sale.surcharge_note = note
            else:
                sale.surcharge_note = False

    surcharge_note = fields.Char(
        string='Surcharge Note',
        compute=_compute_surcharge_note,
    )
