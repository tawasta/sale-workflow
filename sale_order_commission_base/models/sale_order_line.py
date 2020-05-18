
from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    commission = fields.Float(
        string="Commission",
        compute="_compute_commission",
        search="_search_commission",
    )

    @api.multi
    def _search_commission(self, operator, value):
        recs = self.search([]).filtered(
            lambda x: x.commission)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    def _compute_commission(self):
        for line in self:
            line.commission = line.product_id.lst_price * \
                line.product_uom_qty * (1 - (line.discount or 0.0) / 100.0)
