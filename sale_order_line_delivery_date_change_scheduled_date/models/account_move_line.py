from odoo import fields, models


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    line_delivery_date = fields.Datetime(string="Delivery Date")
