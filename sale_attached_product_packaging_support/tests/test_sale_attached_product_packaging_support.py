from odoo import Command
from odoo.tests import TransactionCase


class TestSaleAttachedProductPackagingSupport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_pack_6 = cls.env.ref("uom.product_uom_pack_6")
        cls.partner = cls.env["res.partner"].create({"name": "Test customer"})
        product_model = cls.env["product.product"]
        cls.product_1 = product_model.create(
            {
                "name": "Main",
                "list_price": 50,
                "uom_ids": [Command.set(cls.uom_pack_6.ids)],
            }
        )
        # Allows the 6-pack: follows the main line unit
        cls.product_2 = product_model.create(
            {
                "name": "Deposit",
                "list_price": 60,
                "uom_ids": [Command.set(cls.uom_pack_6.ids)],
            }
        )
        # No 6-pack: keeps its own unit
        cls.product_3 = product_model.create({"name": "Other", "list_price": 70})
        cls.product_1.product_tmpl_id.attached_product_ids = (
            cls.product_2 + cls.product_3
        )
        cls.order = cls.env["sale.order"].create({"partner_id": cls.partner.id})

    def _enable_auto_update(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "sale_attached_product.auto_update_attached_lines", True
        )

    def _get_line(self, product):
        return self.order.order_line.filtered(lambda x: x.product_id == product)

    def _add_main_line(self, uom):
        self.order.write(
            {
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "product_uom_qty": 1,
                            "product_uom_id": uom.id,
                        }
                    )
                ]
            }
        )
        return self._get_line(self.product_1)

    def test_01_attached_line_unit_on_creation(self):
        """Attached lines get the main line unit when allowed, otherwise their own"""
        self._add_main_line(self.uom_pack_6)
        line_2 = self._get_line(self.product_2)
        self.assertEqual(line_2.product_uom_id, self.uom_pack_6)
        self.assertEqual(line_2.product_uom_qty, 1)
        self.assertEqual(line_2.price_unit, 360, "Price of a 6-pack")
        line_3 = self._get_line(self.product_3)
        self.assertEqual(line_3.product_uom_id, self.uom_unit)
        self.assertEqual(line_3.product_uom_qty, 1)
        self.assertEqual(line_3.price_unit, 70)

    def test_02_main_line_unit_change(self):
        """With auto update, attached lines follow a main line unit change and are
        repriced in the new unit"""
        self._enable_auto_update()
        main_line = self._add_main_line(self.uom_unit)
        line_2 = self._get_line(self.product_2)
        self.assertEqual(line_2.product_uom_id, self.uom_unit)
        self.assertEqual(line_2.price_unit, 60)
        main_line.product_uom_id = self.uom_pack_6
        self.assertEqual(line_2.product_uom_id, self.uom_pack_6)
        self.assertEqual(line_2.price_unit, 360, "Repriced for a 6-pack")
        self.assertEqual(self._get_line(self.product_3).product_uom_id, self.uom_unit)

    def test_03_confirmed_order_unit_unchanged(self):
        """A unit change on a confirmed order does not change the attached units"""
        self._enable_auto_update()
        main_line = self._add_main_line(self.uom_unit)
        self.order.action_confirm()
        main_line.product_uom_id = self.uom_pack_6
        self.assertEqual(self._get_line(self.product_2).product_uom_id, self.uom_unit)

    def test_04_unit_change_saved_through_order(self):
        """A unit change saved through the order (as the form does) is followed,
        also when another line already has the new unit"""
        self._enable_auto_update()
        self._add_main_line(self.uom_pack_6)
        main_line = self._add_main_line(self.uom_unit).filtered(
            lambda x: x.product_uom_id == self.uom_unit
        )
        self.order.write(
            {
                "order_line": [
                    Command.update(main_line.id, {"product_uom_id": self.uom_pack_6.id})
                ]
            }
        )
        deposit_line = main_line.attached_line_ids.filtered(
            lambda x: x.product_id == self.product_2
        )
        self.assertEqual(deposit_line.product_uom_id, self.uom_pack_6)
