from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        # Override invoice and delivery address onchange and suggest the
        # main customer for both fields

        values = dict(
            partner_invoice_id=self.partner_id and self.partner_id.id or False,
            partner_shipping_id=self.partner_id and self.partner_id.id or False,
        )

        super(SaleOrder, self).onchange_partner_id()
        self.update(values)
