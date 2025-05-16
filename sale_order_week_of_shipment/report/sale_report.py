from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=True,
    )

    def _select_sale(self):
        select = super()._select_sale()
        select += "%s" % (", s.week_of_shipment AS week_of_shipment")
        return select

    def _group_by_sale(self):
        group_by = super()._group_by_sale()
        group_by += "%s" % (", s.week_of_shipment")
        return group_by
