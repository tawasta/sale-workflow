from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    sale_warn_level = fields.Selection(
        selection=[
            ("warning", "Warning"),
            ("popup_warning", "Popup Warning"),
            ("blocking_warning", "Blocking Warning"),
        ],
        string="Sale Warning Level",
        default="popup_warning",
    )
