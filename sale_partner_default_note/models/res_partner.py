from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    sale_note = fields.Text(string="Sale note", help="Default sale note")
