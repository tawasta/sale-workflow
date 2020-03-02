from odoo import fields, models


class SaleConfigSettings(models.TransientModel):

    _inherit = "sale.config.settings"

    customer_order_number_to_invoice = fields.Boolean(
        related="company_id.customer_order_number_to_invoice",
        string="Pass Customer Order Number to Invoice",
    )
