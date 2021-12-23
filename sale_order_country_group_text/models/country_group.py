from odoo import fields, models


class CountryGroup(models.Model):

    _inherit = "res.country.group"

    sale_order_text = fields.Text(
        string="Sale Order Text",
        help="Text to be added on sales orders going to customers in this "
        + "country group.",
        translate=True,
    )
