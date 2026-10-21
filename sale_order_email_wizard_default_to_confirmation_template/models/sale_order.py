from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _find_mail_template(self):
        """Suggest the order confirmation template as the default of the email
        wizard also for quotations, instead of the quotation template."""
        return self._get_confirmation_template() or super()._find_mail_template()
