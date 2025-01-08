from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sale_order_line_copy_mode = fields.Selection(
        selection=[
            ("directly_after", "Directly after the Original"),
            ("end_of_order", "End of Sale Order"),
        ],
        default="end_of_order",
        config_parameter="sale_order_line_copy.sale_order_line_copy_mode",
        string="Sale Order Line Positioning after Copying",
        help="Where the copied individual SO lines gets placed. "
        "Note: Sections always get placed at the end of Sale Order.",
    )
