from odoo import fields, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    invoice_date = fields.Date(related="invoice_lines.date", store=True, readonly=True)
