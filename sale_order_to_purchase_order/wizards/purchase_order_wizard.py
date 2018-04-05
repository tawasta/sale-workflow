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
            'fiscal_position_id': False,
        }

        # Trigger onchanges programmatically to get fiscal position
        po_spec = purchase_order_model._onchange_spec()
        updates = purchase_order_model.onchange(initial_values,
                                                ['partner_id'],
                                                po_spec)

        onchange_values = updates.get('value', {})
        for name, val in onchange_values.iteritems():
            if isinstance(val, tuple):
                onchange_values[name] = val[0]

        initial_values.update(onchange_values)
        res = purchase_order_model.create(initial_values)
        return res

    def create_purchase_line(self, current_sale_line, purchase_order):

        purchase_order_line_model = self.env['purchase.order.line']

        initial_values = {
            'order_id': purchase_order.id,
            'product_id': current_sale_line.product_id.id,
            'product_qty': current_sale_line.product_uom_qty,
            'product_uom': current_sale_line.product_uom.id,
            'partner_id': purchase_order.partner_id.id,
            'price_unit': False,
            'name': False,
            'date_planned': False,
            'taxes_id': False,
        }

        # Trigger onchanges programmatically to get price, product name,
        # planned date and taxes.
        po_line_spec = purchase_order_line_model._onchange_spec()
        updates = purchase_order_line_model.onchange(initial_values,
                                                     ['product_id'],
                                                     po_line_spec)

        onchange_values = updates.get('value', {})
        for name, val in onchange_values.iteritems():
            if isinstance(val, tuple):
                onchange_values[name] = val[0]

        initial_values.update(onchange_values)

        purchase_order_line_model.create(initial_values)

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

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Supplier',
        domain=[('supplier', '=', True)],
        required=True
    )

    picking_type_id = fields.Many2one(
        comodel_name='stock.picking.type',
        string='Delivery Location',
        required=True,
        default=_get_default_picking_type
    )
