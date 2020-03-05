from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_finalization(self):
        self.state = "finalization"

    state = fields.Selection(
        [
            ("draft", "Quotation"),
            ("sent", "Quotation Sent"),
            ("finalization", "Finalization"),
            ("sale", "Sales Order"),
            ("done", "Locked"),
            ("cancel", "Cancelled"),
        ]
    )

    # Update core's sale module's fields state-based permissions to apply also
    # to the new state so that those fields that were writable in draft and
    # sent states, are now writable also in finalization state
    date_order = fields.Datetime(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )

    validity_date = fields.Date(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )

    partner_id = fields.Many2one(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )
    partner_invoice_id = fields.Many2one(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )
    partner_shipping_id = fields.Many2one(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )
    pricelist_id = fields.Many2one(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )
    project_id = fields.Many2one(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )
    order_line = fields.One2many(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )
