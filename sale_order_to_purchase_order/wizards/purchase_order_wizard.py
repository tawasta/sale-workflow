# -*- coding: utf-8 -*-
from odoo import models, fields


class PurchaseOrderWizard(models.TransientModel):

    _name = "sale_order_to_purchase_order.po_wizard"

    def create_purchase(self, current_sale):

        purchase_order_model = self.env['purchase.order']

        initial_values = {
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'sale_order_id': current_sale.id,
        }

        updated_values = purchase_order_model.play_onchanges(
            initial_values, ['partner_id']
        )

        return purchase_order_model.create(updated_values)

    def create_purchase_line(self, current_sale_line, purchase_order):

        purchase_order_line_model = self.env['purchase.order.line']

        initial_values = {
            'order_id': purchase_order.id,
            'product_id': current_sale_line.product_id.id,
            'product_qty': current_sale_line.product_uom_qty,
            'product_uom': current_sale_line.product_uom.id,
            'partner_id': purchase_order.partner_id.id
        }

        updated_values = purchase_order_line_model.play_onchanges(
            initial_values, ['product_id']
        )

        # Price is mandatory, so set is as 0 in case no
        # supplier price was found
        if 'price_unit' not in updated_values:
            updated_values['price_unit'] = 0.00

        return purchase_order_line_model.create(updated_values)

    def button_create_po(self):

        current_sale = self.env['sale.order'] \
            .browse(self.env.context['active_id'])
        po_res = self.create_purchase(current_sale)

        for so_line in current_sale.order_line:
            self.create_purchase_line(so_line, po_res)

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'res_id': po_res.id,
            'context': self.env.context,
        }

    def _get_default_picking_type(self):
        args = [('code', '=', 'incoming'),
                ('warehouse_id', '=', self.env.context['warehouse_id'])
                ]

        res = self.env['stock.picking.type'] \
            .search(args=args, limit=1)
        return res and res[0] or False

    def _get_default_customer(self):
        return self.env.context.get('customer_id', False)

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Supplier',
        domain=[('supplier', '=', True)],
        required=True
    )

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        readonly=True,
        default=_get_default_customer
    )

    picking_type_id = fields.Many2one(
        comodel_name='stock.picking.type',
        string='Delivery Location',
        required=True,
        default=_get_default_picking_type
    )
