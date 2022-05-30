from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    year_of_shipment = fields.Char(
        string="Year of shipment",
        compute="_compute_delivery_year"
    )

    def _compute_delivery_year(self):
        """Compute method for Year of shipment-field"""
        for sale in self:
            sale.year_of_shipment = sale.commitment_date and \
                    str(sale.commitment_date.year)

    @api.onchange("commitment_date")
    def onchange_shipment_year(self):
        """User-friendly Onchange method for Year of shipment-field"""
        for sale in self:
            sale.year_of_shipment = sale.commitment_date and \
                    str(sale.commitment_date.year)
