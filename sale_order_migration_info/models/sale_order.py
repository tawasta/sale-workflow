from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    migrated = fields.Boolean("Migrated")
    migrated_date = fields.Datetime("Migration Date")
    migrated_comment = fields.Char("Migration Comment")
