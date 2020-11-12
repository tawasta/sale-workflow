
from odoo import fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    # Set store to True so that the grouping works. Else Odoo gives an error
    analytic_tag_name = fields.Char(related='analytic_tag_ids.name', store=True)
