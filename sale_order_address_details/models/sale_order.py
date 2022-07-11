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

    # Invoice address
    partner_invoice_street = fields.Char(
        related="partner_invoice_id.street",
    )

    partner_invoice_street2 = fields.Char(
        related="partner_invoice_id.street2",
    )

    partner_invoice_zip = fields.Char(
        related="partner_invoice_id.zip",
    )

    partner_invoice_city = fields.Char(
        related="partner_invoice_id.city",
    )

    partner_invoice_country_id = fields.Many2one(
        comodel_name="res.country",
        related="partner_invoice_id.country_id",
    )

    # Delivery address
    partner_shipping_street = fields.Char(
        related="partner_shipping_id.street",
    )

    partner_shipping_street2 = fields.Char(
        related="partner_shipping_id.street2",
    )

    partner_shipping_zip = fields.Char(
        related="partner_shipping_id.zip",
    )

    partner_shipping_city = fields.Char(
        related="partner_shipping_id.city",
    )

    partner_shipping_country_id = fields.Many2one(
        comodel_name="res.country",
        related="partner_shipping_id.country_id",
    )
