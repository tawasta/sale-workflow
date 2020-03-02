from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    # Update core's sale_stock module's fields' state-based permissions to
    # apply also to the new state so that those fields that were writable
    # in draft and sent states, are now writable also in finalization state
    picking_policy = fields.Selection(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )

    warehouse_id = fields.Many2one(
        states={
            "draft": [("readonly", False)],
            "sent": [("readonly", False)],
            "finalization": [("readonly", False)],
        }
    )
