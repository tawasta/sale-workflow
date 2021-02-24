from odoo import fields, models
from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):

    _inherit = "sale.order"

    weight = fields.Float(
        "Weight", digits=dp.get_precision("Stock Weight"), compute="_compute_weight"
    )

    def _compute_weight(self):
        for record in self:
            weight = 0
            for line in record.order_line:
                weight += line.weight

            record.weight = weight
