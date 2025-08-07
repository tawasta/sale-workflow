from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("partner_id")
    def _compute_payment_term_id(self):
        super()._compute_payment_term_id()

        for sale in self:
            default_payment_term = sale.company_id.sale_default_payment_term

            if not sale.payment_term_id and default_payment_term and sale.partner_id:
                sale.payment_term_id = default_payment_term
