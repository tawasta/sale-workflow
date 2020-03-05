from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.onchange("incoterm")
    def onchange_incoterm(self):
        """ Append the shipping address' name to the extra info field,
        if the incoterm so indicates """
        if (
            self.partner_shipping_id
            and self.incoterm
            and self.incoterm.append_partner_name
        ):
            self.incoterm_extra_info = self.partner_shipping_id.name
        else:
            self.incoterm_extra_info = False

    incoterm_extra_info = fields.Char(
        string="Incoterms additional info",
        help="""Use for storing e.g. the pickup location""",
    )
