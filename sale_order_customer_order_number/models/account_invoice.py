from odoo import fields, models


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    # Legacy field, not shown anymore, and to be removed
    customer_order_number = fields.Char(
        string="Customer's Order Number",
        help="""If the customer has specified an order number of their own""",
    )
