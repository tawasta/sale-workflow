from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    show_sale_header = fields.Boolean(
        "Show header on report",
        config_parameter="sale.show_sale_header",
        help="Show header value on Sale Report.",
    )
