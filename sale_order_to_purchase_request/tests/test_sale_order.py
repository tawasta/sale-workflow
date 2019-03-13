# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestSale(TransactionCase):

    def setUp(self):
        '''Set up some test data. This will be
        available for all the actual test methods'''
        res = super(TestSale, self).setUp()

        partner_model = self.env['res.partner']
        product_model = self.env['product.product']
        sale_order_model = self.env['sale.order']
        stock_location_model = self.env['stock.location']

        payment_term = self.env.ref('account.account_payment_term_net')

        # Routes
        self.buy_route = self.env.ref('purchase.route_warehouse0_buy')
        self.manufacture_route \
            = self.env.ref('mrp.route_warehouse0_manufacture')

        # UOMs
        self.uom_unit = self.env.ref('product.product_uom_unit')
        self.uom_dozen = self.env.ref('product.product_uom_dozen')

        # Stock locations
        self.common_location = self.env.ref('stock.stock_location_stock')
        self.project_location = stock_location_model.create({
            'name': 'Project location'
        })

        # Company & settings
        self.main_company = self.env.ref('base.main_company')
        self.main_company.purchase_request_from_sale_buy = True
        self.main_company.purchase_request_from_sale_mrp = True
        self.main_company.purchase_request_location_rule = 'project_and_custom'
        self.main_company.purchase_request_location_ids \
            = [(6, 0, [self.common_location.id, self.project_location.id])]

        # Partner
        self.partner_1 = partner_model.create({
            'name': 'Test Customer'
        })

        # Products
        self.main_assembly_1 = product_model.create({
            'name': 'Main assembly 1',
            'route_ids': [(6, 0, [self.manufacture_route.id])],
            'purchase_line_warn': 'no-message'})

        self.main_assembly_2 = product_model.create({
            'name': 'Main assembly 2',
            'route_ids': [(6, 0, [self.manufacture_route.id])],
            'purchase_line_warn': 'no-message'})

        self.subassembly_1 = product_model.create({
            'name': 'Sub-assembly 1',
            'route_ids': [(6, 0, [self.manufacture_route.id])],
            'purchase_line_warn': 'no-message'})

        self.subassembly_2 = product_model.create({
            'name': 'Sub-assembly 2',
            'route_ids': [(6, 0, [self.manufacture_route.id])],
            'purchase_line_warn': 'no-message'})

        self.subassembly_3 = product_model.create({
            'name': 'Sub-assembly 3',
            'route_ids': [(6, 0, [self.manufacture_route.id])],
            'purchase_line_warn': 'no-message'})

        self.component_1 = product_model.create({
            'name': 'Component 1',
            'route_ids': [(6, 0, [self.buy_route.id])],
            'purchase_line_warn': 'no-message'})

        self.component_2 = product_model.create({
            'name': 'Component 2',
            'route_ids': [(6, 0, [self.buy_route.id])],
            'purchase_line_warn': 'no-message'})

        self.component_3 = product_model.create({
            'name': 'Component 3',
            'route_ids': [(6, 0, [self.buy_route.id])],
            'purchase_line_warn': 'no-message'})

        # Main assembly BOM
        # Main assembly
        #  - Component1 x 5
        #  - Component2 x 5
        #  - Component2 x 5
        bom_res = self.env['mrp.bom'].create({
            'product_tmpl_id': self.main_assembly_1.product_tmpl_id.id
        })
        self.env['mrp.bom.line'].create({
            'bom_id': bom_res.id,
            'product_id': self.component_1.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 5
        })
        self.env['mrp.bom.line'].create({
            'bom_id': bom_res.id,
            'product_id': self.component_2.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 5
        })
        self.env['mrp.bom.line'].create({
            'bom_id': bom_res.id,
            'product_id': self.component_2.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 5
        })

        # Main assembly2 BOM
        # Main assembly2
        #  - Component1 x 1 units
        #  - Component2 x 2 units
        #  - Sub-assembly1 x 2 units
        #    - Component1 x 1 units
        #    - Component3 x 3 units
        #  - Sub-assembly2 x 2 units
        #    - Component1 x 1 units
        #    - Component3 x 3 units
        #    - Sub-assembly3 x 3 units
        #      - Component2 x 2 units
        #      - Sub-assembly1 x 2 units
        #        - Component1 x 1 units
        #        - Component3 x 3 units
        #
        # Expected totals:
        # - Component 1: 1 + (2*1) + (2*1) + (2*3*2*1) = 17
        # - Component 2: 2 + (2*3*2) = 14
        # - Component 3: (2*3) + (2*3) + (2*3*2*3) = 48

        subassembly_1_bom_res = self.env['mrp.bom'].create({
            'product_tmpl_id': self.subassembly_1.product_tmpl_id.id
        })
        self.env['mrp.bom.line'].create({
            'bom_id': subassembly_1_bom_res.id,
            'product_id': self.component_1.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 1
        })
        self.env['mrp.bom.line'].create({
            'bom_id': subassembly_1_bom_res.id,
            'product_id': self.component_3.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 3
        })

        subassembly_3_bom_res = self.env['mrp.bom'].create({
            'product_tmpl_id': self.subassembly_3.product_tmpl_id.id
        })
        self.env['mrp.bom.line'].create({
            'bom_id': subassembly_3_bom_res.id,
            'product_id': self.component_2.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 2
        })
        self.env['mrp.bom.line'].create({
            'bom_id': subassembly_3_bom_res.id,
            'product_id': self.subassembly_1.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 2
        })

        subassembly_2_bom_res = self.env['mrp.bom'].create({
            'product_tmpl_id': self.subassembly_2.product_tmpl_id.id
        })
        self.env['mrp.bom.line'].create({
            'bom_id': subassembly_2_bom_res.id,
            'product_id': self.component_1.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 1
        })
        self.env['mrp.bom.line'].create({
            'bom_id': subassembly_2_bom_res.id,
            'product_id': self.component_3.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 3
        })
        self.env['mrp.bom.line'].create({
            'bom_id': subassembly_2_bom_res.id,
            'product_id': self.subassembly_3.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 3
        })

        main_assembly_2_bom_res = self.env['mrp.bom'].create({
            'product_tmpl_id': self.main_assembly_2.product_tmpl_id.id
        })
        self.env['mrp.bom.line'].create({
            'bom_id': main_assembly_2_bom_res.id,
            'product_id': self.component_1.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 1
        })
        self.env['mrp.bom.line'].create({
            'bom_id': main_assembly_2_bom_res.id,
            'product_id': self.component_2.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 2
        })
        self.env['mrp.bom.line'].create({
            'bom_id': main_assembly_2_bom_res.id,
            'product_id': self.subassembly_1.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 2
        })
        self.env['mrp.bom.line'].create({
            'bom_id': main_assembly_2_bom_res.id,
            'product_id': self.subassembly_2.id,
            'product_uom_id': self.uom_unit.id,
            'product_qty': 2
        })

        # Sale order 1 with main assembly
        self.sale_1 = sale_order_model.create({
            'partner_id': self.partner_1.id,
            'payment_term_id': payment_term.id,
        })

        self.env['sale.order.line'].create({
            'product_id': self.main_assembly_1.id,
            'product_uom_qty': 1,
            'product_uom': self.uom_unit.id,
            'order_id': self.sale_1.id,
        })

        # Sale order 2 with no manufacturing, just components to sell
        self.sale_2 = sale_order_model.create({
            'partner_id': self.partner_1.id,
            'payment_term_id': payment_term.id,
        })

        self.env['sale.order.line'].create({
            'product_id': self.component_1.id,
            'name': 'Component 1',
            'product_uom_qty': 10,
            'product_uom': self.uom_unit.id,
            'order_id': self.sale_2.id,
        })

        self.env['sale.order.line'].create({
            'product_id': self.component_1.id,
            'name': 'Component 1 with a different description',
            'product_uom_qty': 5,
            'product_uom': self.uom_unit.id,
            'order_id': self.sale_2.id,
        })

        self.env['sale.order.line'].create({
            'product_id': self.component_2.id,
            'name': 'Component 2',
            'product_uom_qty': 20,
            'product_uom': self.uom_unit.id,
            'order_id': self.sale_2.id,
        })

        # Sale order 3 with main assembly 2 and individual components
        self.sale_3 = sale_order_model.create({
            'partner_id': self.partner_1.id,
            'payment_term_id': payment_term.id,
        })

        self.env['sale.order.line'].create({
            'product_id': self.main_assembly_2.id,
            'product_uom_qty': 1,
            'product_uom': self.uom_unit.id,
            'order_id': self.sale_3.id,
        })

        self.env['sale.order.line'].create({
            'product_id': self.component_1.id,
            'name': 'Component 1',
            'product_uom_qty': 10,
            'product_uom': self.uom_unit.id,
            'order_id': self.sale_3.id,
        })

        return res

    def test_manufacturables_empty_stock(self):
        '''Test calculated PR quantities for a manufacturable
        when the stock is empty '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Confirm the order
        self.sale_1.action_confirm()

        self.assertTrue(self.sale_1.purchase_request_id,
                        'Purchase request should have been created')
        self.assertEquals(len(self.sale_1.purchase_request_id.line_ids), 2,
                          'The purchase request should have 2 lines')

        products_to_check = [(self.component_1, 5),
                             (self.component_2, 10)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_1.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials for ' +
                              'purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request ' +
                              'line per product')

    def test_manufacturables_full_stock(self):
        '''Test a manufacturable when everything is in stock '''

        # Update Inventory so that both components are in stock
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        self.env['stock.change.product.qty'].create({
            'product_id': self.component_2.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        # Confirm the order
        self.sale_1.action_confirm()

        self.assertFalse(self.sale_1.purchase_request_id,
                         'Purchase request should not have been created')

    def test_manufacturables_partial_stock(self):
        '''Test a manufacturable when one of the products is in stock '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Update Inventory
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        # Confirm the order
        self.sale_1.action_confirm()

        self.assertTrue(self.sale_1.purchase_request_id,
                        'Purchase request should have been created')
        self.assertEquals(len(self.sale_1.purchase_request_id.line_ids), 1,
                          'The purchase request should have 1 line')

        products_to_check = [(self.component_2, 10)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_1.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials for ' +
                              'purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request ' +
                              'line per product')

    def test_manufacturables_partial_stock_partial_qty(self):
        '''Test a manufacturable when products are in stock but there
        is not enough qty '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Update Inventory
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 2,
        }).change_product_qty()

        self.env['stock.change.product.qty'].create({
            'product_id': self.component_2.id,
            'location_id': self.common_location.id,
            'new_quantity': 3,
        }).change_product_qty()

        # Confirm the order
        self.sale_1.action_confirm()

        self.assertTrue(self.sale_1.purchase_request_id,
                        'Purchase request should have been created')
        self.assertEquals(len(self.sale_1.purchase_request_id.line_ids), 2,
                          'The purchase request should have 2 lines')

        products_to_check = [(self.component_1, 3),
                             (self.component_2, 7)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_1.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials ' +
                              'for purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request ' +
                              'line per product')

    def test_purchasables_empty_stock(self):
        '''Test calculated PR quantities for a purchasable
        when the stock is empty '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Confirm the order
        self.sale_2.action_confirm()

        self.assertTrue(self.sale_2.purchase_request_id,
                        'Purchase request should have been created')
        self.assertEquals(len(self.sale_2.purchase_request_id.line_ids), 2,
                          'The purchase request should have 2 lines')

        products_to_check = [(self.component_1, 15),
                             (self.component_2, 20)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_2.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials for ' +
                              'purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request ' +
                              'line per product')

    def test_purchasables_full_stock(self):
        '''Test a purchasable when everything is in stock '''

        # Update Inventory so that both components are in stock
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        self.env['stock.change.product.qty'].create({
            'product_id': self.component_2.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        # Confirm the order
        self.sale_1.action_confirm()

        self.assertFalse(self.sale_1.purchase_request_id,
                         'Purchase request should not have been created')

    def test_purchasables_partial_stock(self):
        '''Test a purchasable when one of the products is in stock '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Update Inventory
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        # Confirm the order
        self.sale_2.action_confirm()

        self.assertTrue(self.sale_2.purchase_request_id,
                        'Purchase request should have been created')
        self.assertEquals(len(self.sale_2.purchase_request_id.line_ids), 1,
                          'The purchase request should have 1 line')

        products_to_check = [(self.component_2, 20)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_2.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials for ' +
                              'purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request ' +
                              'line per product')

    def test_purchasables_partial_stock_partial_qty(self):
        '''Test a purchasable when products are in stock but there
        is not enough qty '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Update Inventory
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 2,
        }).change_product_qty()

        self.env['stock.change.product.qty'].create({
            'product_id': self.component_2.id,
            'location_id': self.common_location.id,
            'new_quantity': 3,
        }).change_product_qty()

        # Confirm the order
        self.sale_2.action_confirm()

        self.assertTrue(self.sale_2.purchase_request_id,
                        'Purchase request should have been created')
        self.assertEquals(len(self.sale_2.purchase_request_id.line_ids), 2,
                          'The purchase request should have 2 lines')

        products_to_check = [(self.component_1, 13),
                             (self.component_2, 17)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_2.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials for ' +
                              'purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request line ' +
                              'per product')

    def test_purchasables_manufacturables_empty_stock(self):
        '''Test calculated PR quantities for a sale order containing
        both purchasables and manufacturables when the stock is empty '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Confirm the order
        self.sale_3.action_confirm()

        self.assertTrue(self.sale_3.purchase_request_id,
                        'Purchase request should have been created')

        products_to_check = [(self.component_1, 27),
                             (self.component_2, 14),
                             (self.component_3, 48)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_3.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials for ' +
                              'purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request line ' +
                              'per product')

    def test_purchasables_manufacturables_full_stock(self):
        '''Test calculated PR quantities for a sale order containing
        both purchasables and manufacturables when everything in stock '''

        # Update Inventory so that all components are in stock
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        self.env['stock.change.product.qty'].create({
            'product_id': self.component_2.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        self.env['stock.change.product.qty'].create({
            'product_id': self.component_3.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        # Confirm the order
        self.sale_1.action_confirm()

        self.assertFalse(self.sale_3.purchase_request_id,
                         'Purchase request should not have been created')

    def test_purchasables_manufacturables_partial_stock(self):
        '''Test calculated PR quantities for a sale order containing
        both purchasables and manufacturables when one product in stock '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Update Inventory
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 100,
        }).change_product_qty()

        # Confirm the order
        self.sale_3.action_confirm()

        self.assertTrue(self.sale_3.purchase_request_id,
                        'Purchase request should have been created')
        self.assertEquals(len(self.sale_3.purchase_request_id.line_ids), 2,
                          'The purchase request should have 2 lines')

        products_to_check = [(self.component_2, 14),
                             (self.component_3, 48)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_3.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials for ' +
                              'purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request line ' +
                              'per product')

    def test_purchasables_manufacturables_partial_stock_partial_qty(self):
        '''Test calculated PR quantities for a sale order containing
        both purchasables and manufacturables when one product is
        partially in stock '''

        purchase_request_line_model = self.env['purchase.request.line']

        # Update Inventory
        self.env['stock.change.product.qty'].create({
            'product_id': self.component_1.id,
            'location_id': self.common_location.id,
            'new_quantity': 2,
        }).change_product_qty()

        self.env['stock.change.product.qty'].create({
            'product_id': self.component_2.id,
            'location_id': self.common_location.id,
            'new_quantity': 3,
        }).change_product_qty()

        self.env['stock.change.product.qty'].create({
            'product_id': self.component_3.id,
            'location_id': self.common_location.id,
            'new_quantity': 10,
        }).change_product_qty()

        # Confirm the order
        self.sale_3.action_confirm()

        self.assertTrue(self.sale_3.purchase_request_id,
                        'Purchase request should have been created')
        self.assertEquals(len(self.sale_3.purchase_request_id.line_ids), 3,
                          'The purchase request should have 3 lines')

        products_to_check = [(self.component_1, 25),
                             (self.component_2, 11),
                             (self.component_3, 38)]

        for p in products_to_check:
            args = [('request_id', '=', self.sale_3.purchase_request_id.id),
                    ('product_id', '=', p[0].id)]
            pr_lines = purchase_request_line_model.search(args)
            self.assertEquals(pr_lines[0].product_qty, p[1],
                              'Wrong amount of raw materials for ' +
                              'purchase request')
            self.assertEquals(len(pr_lines), 1,
                              'There should be one purchase request line ' +
                              'per product')
