from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def validate_pickings_then_create_and_post_invoice(self):
        """@Return:
        1. Verify and Confirm SO.
        2. Delivery order sets to done.
        3. Create an invoice.
        4. Validate an invoice.
        """
        self.action_confirm()
        invoices = []
        for order in self:
            for picking in order.picking_ids:
                picking.action_assign()
                picking.action_confirm()
                picking.button_validate()

            order._create_invoices()
            for invoice in order.invoice_ids:
                invoice.action_post()

        # Display invoice view after confirm sales order.
        invoices.extend(order.invoice_ids.ids)
        if invoices:
            action = {
                "name": _("Invoices"),
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
                    "name": _("Invoices"),
                    "res_id": invoices[0],
                    "res_model": "account.move",
                    "view_mode": "form",
                    "view_type": "tree",
                    "type": "ir.actions.act_window",
                    "views": [(self.env.ref("account.view_move_form").id, "form")],
                }
            return action
        return True
