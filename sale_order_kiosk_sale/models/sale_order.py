from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # pylint: disable=E8102
    def process_picking_and_payment(self):
        """
        1. Verify and Confirm SO.
        2. Delivery order sets to done.
        3. Create an invoice.
        4. Validate an invoice.
        5. Set invoice as paid.
        """
        self.action_confirm()
        invoices = []
        for order in self:
            failed_pickings = self.env["stock.picking"]

            for picking in order.picking_ids:
                picking.action_assign()
                picking.action_confirm()

                try:
                    with self.env.cr.savepoint():
                        picking.button_validate()

                        if picking.state != "done":
                            failed_pickings |= picking
                except Exception:
                    failed_pickings |= picking

            if failed_pickings:
                self.env.cr.commit()

                message = self.env._(
                    "Sale has been confirmed, but Picking could not be validated."
                )
                message_wiz = self.env["sale.order.kiosk.message"].create(
                    {"message": message}
                )

                return {
                    "type": "ir.actions.act_window",
                    "res_model": "sale.order.kiosk.message",
                    "view_type": "form",
                    "view_mode": "form",
                    "res_id": message_wiz.id,
                    "target": "new",
                }

            order._create_invoices()

            for invoice in order.invoice_ids:
                invoice.action_post()

                journal_id = self.env["account.journal"].search(
                    [("type", "in", ("cash"))],
                    limit=1,
                )

                try:
                    with self.env.cr.savepoint():
                        self.env["account.payment.register"].with_context(
                            active_model="account.move",
                            active_ids=[invoice.id],
                            default_journal_id=(journal_id and journal_id.id or None),
                        ).create({"group_payment": False}).action_create_payments()
                except Exception:
                    self.env.cr.commit()

                    message = self.env._("Invoice could not be paid")
                    message_wiz = self.env["sale.order.kiosk.message"].create(
                        {"message": message}
                    )

                    return {
                        "type": "ir.actions.act_window",
                        "res_model": "sale.order.kiosk.message",
                        "view_type": "form",
                        "view_mode": "form",
                        "res_id": message_wiz.id,
                        "target": "new",
                    }

        # Display invoice view after confirm sales order.
        invoices.extend(order.invoice_ids.ids)
        if invoices:
            action = {
                "name": self.env._("Invoices"),
                "domain": [("id", "in", invoices)],
                "res_model": "account.move",
                "view_mode": "tree,form",
                "type": "ir.actions.act_window",
                "views": [
                    (self.env.ref("account.view_move_tree").id, "tree"),
                    (False, "form"),
                ],
            }
            if len(invoices) == 1:
                action = {
                    "name": self.env._("Invoices"),
                    "res_id": invoices[0],
                    "res_model": "account.move",
                    "view_mode": "form",
                    "view_type": "tree",
                    "type": "ir.actions.act_window",
                    "views": [(self.env.ref("account.view_move_form").id, "form")],
                }
            return action
        return True
