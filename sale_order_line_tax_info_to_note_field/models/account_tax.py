from odoo import fields, models


class AccountTax(models.Model):

    _inherit = 'account.tax'

    sale_order_note = fields.Text(string="Note to Sale Order")
