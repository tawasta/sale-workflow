# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions, _
from math import ceil


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = 'sale.order'

    # 2. Fields
    purchase_request_id = fields.Many2one(
        comodel_name='purchase.request',
        string='Purchase Request',
        help='''Purchase Request containing this order's components'''
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_confirm(self):
        '''Check the need for a new purchase request when the sale order is
        confirmed'''

        res = super(SaleOrder, self).action_confirm()

        purchaseables = self.get_purchaseables()
        manufacturables = self.get_manufacturables()

        if (self.company_id.purchase_request_from_sale_mrp or
            self.company_id.purchase_request_from_sale_buy) \
                and (manufacturables or purchaseables):

            self.create_purchase_request(purchaseables, manufacturables)

        return res

    # 8. Business methods
    def get_purchaseables(self):
        '''Get those products on sale order lines that have a purchase route
        but no manufacturing route '''
        buy_route = self.env.ref('purchase.route_warehouse0_buy',
                                 raise_if_not_found=False)

        manufacture_route = self.env.ref('mrp.route_warehouse0_manufacture',
                                         raise_if_not_found=False)

        purchaseables = []

        for sale_line in self.order_line:
            if buy_route in sale_line.product_id.route_ids \
                    and manufacture_route not in \
                    sale_line.product_id.route_ids:
                purchaseables.append(sale_line)

        return purchaseables

    def get_manufacturables(self):
        '''Get those products on sale order lines that have a manufacture route
        but no buy route '''
        buy_route = self.env.ref('purchase.route_warehouse0_buy',
                                 raise_if_not_found=False)

        manufacture_route = self.env.ref('mrp.route_warehouse0_manufacture',
                                         raise_if_not_found=False)

        manufacturables = []

        for sale_line in self.order_line:
            if manufacture_route in sale_line.product_id.route_ids \
                    and buy_route not in sale_line.product_id.route_ids \
                    and sale_line.product_id.bom_ids:
                manufacturables.append(sale_line)

        return manufacturables

    def prepare_purchase_request_values(self):
        '''Form a dictionary of field values to pass to the created
        Purchase Request'''
        vals = {
            'origin': self.name,
            'requested_by': self.user_id.id,
            'analytic_account_id': self.project_id.id,
            'stock_location_id': self.stock_location_id.id
        }
        return vals

    def create_purchase_request(self, purchaseables, manufacturables):
        '''Compare the needed quantities to available quantities and create
        a purchase request with corresponding quantities'''

        purchase_request_model = self.env['purchase.request']
        purchase_request_line_model = self.env['purchase.request.line']
        bom_model = self.env['mrp.bom']

        boms_to_compute = []

        for line in manufacturables:
            bom = self.env['mrp.bom']._bom_find(
                product_tmpl=line.product_id.product_tmpl_id,
                product=line.product_id)

            # If for some reason the amount sold on line is a float,
            # round it up to nearest integer
            # for the purposes of calculating required materials
            for i in range(int(ceil(line.product_uom_qty))):
                boms_to_compute.append(bom.id)

        # Get a list containing the total raw material requirements of the
        # sold manufacturables' BOMs
        materials_needed \
            = bom_model.browse(boms_to_compute).compute_raw_material_qties()

        # Go through the list of SO lines that contain products that are sold
        # without manufacturing them. Add them to the total list of needed
        # materials
        for p in purchaseables:
            product_index = \
                next((i for (i, d)
                     in enumerate(materials_needed)
                     if d['product'] == p.product_id), None)

            if product_index is None:
                materials_needed.append({
                    'product': p.product_id,
                    'quantity': p.product_uom_qty
                })
            else:
                materials_needed[product_index]['quantity'] \
                    += p.product_uom_qty

        materials_compared_to_stock = []

        # Go through the total material requirements and compare them to
        # stock levels. Store the quantities
        if self.company_id.purchase_request_location_rule \
                == 'project_and_custom':
            locations_to_check = \
                [l.id for l in
                 self.company_id.purchase_request_location_ids] \
                + [self.project_id.default_location_id.id]

            for material in materials_needed:
                qty_available = material['product'] \
                    .with_context(location=locations_to_check) \
                    .qty_available

                if qty_available < material['quantity']:
                    materials_compared_to_stock.append({
                        'product': material['product'],
                        'quantity': material['quantity'] - qty_available
                    })

            # If stock levels are lower than required for any of the materials,
            # create a purchase request containing one line for each product
            if materials_compared_to_stock:
                pr_values = self.prepare_purchase_request_values()
                pr_res = purchase_request_model.create(pr_values)

                for material in materials_compared_to_stock:
                    if material['product'].type == 'product':
                        purchase_request_line_model.create({
                            'request_id': pr_res.id,
                            'product_id': material['product'].id,
                            'product_uom_id': material['product'].uom_id.id,
                            'product_qty': material['quantity']
                        })

                # Link the new purchase request to the sale order
                self.purchase_request_id = pr_res.id
        else:
            raise exceptions \
                .UserError(_('Unimplemented "Locations to Check" rule'))
