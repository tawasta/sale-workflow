# -*- coding: utf-8 -*-
from odoo import models, api, fields


class StockReturnPicking(models.TransientModel):

    _inherit = 'stock.return.picking'

    '''
    location_id = fields.Many2one(
        default=lambda self: self._default_get_location_id(),
    )

    @api.multi
    def create_returns(self, location_id=False, force_defaults=False):
        # Force location id

        if location_id:
            self.location_id = location_id

        if force_defaults:
            fields = [
                'product_return_moves',
                'move_dest_exists',
                'parent_location_id',
                'original_location_id',
                'location_id',
            ]
            defaults = self.default_get(fields)
            self.write(defaults)

        return super(StockReturnPicking, self).create_returns()

    def _default_get_location_id(self):
        location_id = self._context.get('location_id')

        if location_id:
            return location_id.id
    '''