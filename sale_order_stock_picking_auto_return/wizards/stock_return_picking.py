# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class StockReturnPicking(models.TransientModel):

    _inherit = 'stock.return.picking'

    @api.multi
    def _force_create_returns(self, vals=False):
        # self.write(vals) won't work for some reason
        for key, val in vals.iteritems():
            setattr(self, key, val)

        # TDE FIXME: store it in the wizard, stupid
        picking = self.env['stock.picking'].browse(
            self.env.context['active_id'])

        return_moves = self.product_return_moves.mapped('move_id')

        unreserve_moves = self.env['stock.move']
        for move in return_moves:
            to_check_moves = self.env['stock.move'] | move.move_dest_id
            while to_check_moves:
                current_move = to_check_moves[-1]
                to_check_moves = to_check_moves[:-1]
                if current_move.state not in (
                'done', 'cancel') and current_move.reserved_quant_ids:
                    unreserve_moves |= current_move
                split_move_ids = self.env['stock.move'].search(
                    [('split_from', '=', current_move.id)])
                to_check_moves |= split_move_ids

        if unreserve_moves:
            unreserve_moves.do_unreserve()
            # break the link between moves in order to be able to fix them later
            # if needed
            unreserve_moves.write({'move_orig_ids': False})

        # create new picking for returned products
        picking_type_id = picking.picking_type_id.return_picking_type_id.id \
                          or picking.picking_type_id.id

        new_picking = picking.copy({
            'move_lines': [],
            'picking_type_id': picking_type_id,
            'state': 'draft',
            'origin': picking.name,
            'location_id': picking.location_dest_id.id,
            'location_dest_id': self.location_id.id})

        new_picking.message_post_with_view('mail.message_origin_link',
                                           values={'self': new_picking,
                                                   'origin': picking},
                                           subtype_id=self.env.ref(
                                               'mail.mt_note').id)

        returned_lines = 0
        for move_id in return_moves:
            new_qty = move.product_uom_qty
            if new_qty:
                # The return of a return should be linked with the original's
                # destination move if it was not cancelled
                if move_id.origin_returned_move_id.move_dest_id.id \
                        and move_id.origin_returned_move_id.move_dest_id.state \
                                != 'cancel':
                    move_dest_id = \
                        move_id.origin_returned_move_id.move_dest_id.id
                else:
                    move_dest_id = False

                returned_lines += 1

                move_id.copy({
                    'product_id': move_id.product_id.id,
                    'product_uom_qty': new_qty,
                    'picking_id': new_picking.id,
                    'state': 'draft',
                    'location_id': move_id.location_dest_id.id,
                    'location_dest_id': move_id.location_id.id,
                    'picking_type_id': picking_type_id,
                    'warehouse_id': picking.picking_type_id.warehouse_id.id,
                    'origin_returned_move_id': move_id.id,
                    'procure_method': 'make_to_stock',
                    'move_dest_id': move_dest_id,
                })

        if not returned_lines:
            raise UserError(_("Please specify at least one non-zero quantity."))

        new_picking.action_confirm()
        new_picking.action_assign()

        # Mark all rows as done
        for pick in new_picking.pack_operation_ids:
            pick.qty_done = pick.product_qty

        # Do the transfer
        new_picking.do_new_transfer()

        return new_picking.id, picking_type_id

    @api.multi
    def force_create_returns(self, location_id=False):
        if location_id:
            self.location_id = location_id

        fields = [
            'product_return_moves',
            'move_dest_exists',
            'parent_location_id',
            'original_location_id',
            'location_id',
        ]
        vals = self.default_get(fields)

        for wizard in self:
            new_picking_id, pick_type_id = wizard._force_create_returns(vals)
        # Override the context to disable all the potential filters that
        # could have been set previously
        ctx = dict(self.env.context)
        ctx.update({
            'search_default_picking_type_id': pick_type_id,
            'search_default_draft': False,
            'search_default_assigned': False,
            'search_default_confirmed': False,
            'search_default_ready': False,
            'search_default_late': False,
            'search_default_available': False,
        })
        return {
            'name': _('Returned Picking'),
            'view_type': 'form',
            'view_mode': 'form,tree,calendar',
            'res_model': 'stock.picking',
            'res_id': new_picking_id,
            'type': 'ir.actions.act_window',
            'context': ctx,
        }

