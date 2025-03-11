from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Partner address
    partner_street = fields.Char(
        related="partner_id.street",
    )

    partner_street2 = fields.Char(
        related="partner_id.street2",
    )

    partner_zip = fields.Char(
        related="partner_id.zip",
    )

    partner_city = fields.Char(
        related="partner_id.city",
    )

    partner_country_id = fields.Many2one(
        comodel_name="res.country",
        related="partner_id.country_id",
    )
