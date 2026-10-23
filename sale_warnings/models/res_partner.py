from odoo import fields, models

from odoo.addons.partner_warnings.models.partner_warning_mixin import WARNING_LEVELS


class Partner(models.Model):
    _inherit = "res.partner"

    sale_warn_level = fields.Selection(
        selection=WARNING_LEVELS,
        string="Sale Warning Level",
        default="popup_warning",
    )
