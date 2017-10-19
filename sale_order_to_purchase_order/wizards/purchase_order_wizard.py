# -*- coding: utf-8 -*-
from openerp import models, fields, api, _, exceptions


class PurchaseOrderWizard(models.TransientModel):

    _name = "sale_order_to_purchase_order.po_wizard"

    def create_purchase(self, current_sale):
        # Override to add new fields as necessary
        purchase_order_model = self.env['purchase.order']

        vals = {
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'sale_order_id': current_sale.id,
        }

        # Call core's onchanges so that the rest of field values get initialized
        res = purchase_order_model.create(vals)
        res.onchange_partner_id()
        res._onchange_picking_type_id()
        return res

    def create_purchase_line(self, current_sale_line, purchase_order):
        # Override to add new fields as necessary
        purchase_order_line_model = self.env['purchase.order.line']

        vals = {
            'order_id': purchase_order.id,
            'state': 'draft',
            'product_id': current_sale_line.product_id.id,
            'date_planned': fields.Date.today(),
            'name': current_sale_line.name,
            'partner_id': self.partner_id.id,
            'price_unit': current_sale_line.price_unit,
            'product_qty': current_sale_line.product_uom_qty,
            'product_uom': current_sale_line.product_uom.id
        }

        # Do not call onchange here as we want to preserve the line values. This means that e.g. taxes have to be set manually though
        purchase_order_line_model.create(vals)

    def button_create_po(self):

        current_sale = self.env['sale.order'].browse(self.env.context['active_id'])
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
        res = self.env['stock.picking.type'].search(args=[('code', '=', 'incoming')], limit=1)
        return res and res[0] or False

    partner_id = fields.Many2one('res.partner', string='Supplier', domain=[('supplier', '=', True)], required=True)
    picking_type_id = fields.Many2one('stock.picking.type', string='Delivery Location', domain=[('code', '=', 'incoming')], required=True, default=_get_default_picking_type)