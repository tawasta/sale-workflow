from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        # "Disable" invoice and delivery address onchange
        # Due to the original onchange_partner_id() structure, this is done
        # the dumb way and the change is undone after the method

        values = dict(
            partner_invoice_id=self.partner_invoice_id,
            partner_shipping_id=self.partner_shipping_id,
        )

        super(SaleOrder, self).onchange_partner_id()

        self.update(values)
