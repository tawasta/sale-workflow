from odoo import api, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        # First run onchange method normally
        super().onchange_partner_id()

        # Search all delivery addresses, including company type ones
        shipping_address_ids = self.partner_id.address_ids.filtered(
            lambda x: x.type == 'delivery')

        # Set delivery address as first record from the list
        if shipping_address_ids:
            self.update({
                'partner_shipping_id': shipping_address_ids[0]
            })
