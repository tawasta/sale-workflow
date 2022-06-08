from odoo import fields, models


class CountryGroup(models.Model):

    _inherit = "res.country.group"

    proforma_text = fields.Text(
        string="PRO-FORMA Text",
        help="Text to be added on PRO-FORMA going to customers in this "
        + "country group.",
        translate=True,
    )
