from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = ["sale.order", "partner.warning.mixin"]

    _warning_message_field = "sale_warn_msg"
    _warning_level_field = "sale_warn_level"

    partner_sale_warn_level = fields.Selection(related="partner_id.sale_warn_level")
