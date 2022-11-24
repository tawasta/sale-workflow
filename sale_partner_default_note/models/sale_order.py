from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.onchange("partner_id")
    def onchange_partner_id_update_sale_note(self):
        for record in self:
            if record.partner_id and record.partner_id.sale_note:
                record.note = record.partner_id.sale_note
