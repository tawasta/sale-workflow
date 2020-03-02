from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    partner_shipping_id_keep = fields.Boolean(
        string="Keep shipping address", default=True
    )

    @api.multi
    def action_confirm(self):
        if (
            not self.partner_shipping_id_keep
            and self.partner_shipping_id.type == "delivery"
        ):
            self.partner_shipping_id.active = False

        return super(SaleOrder, self).action_confirm()
