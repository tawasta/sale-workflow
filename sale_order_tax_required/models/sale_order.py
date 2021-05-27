from odoo import api
from odoo import models
from odoo import _
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):

        errors = []
        error_template = _("Order has a line with product '%s' with no taxes")
        for line in self.mapped("order_line").filtered(lambda x: not x.display_type):
            if not line.tax_id:
                error_string = error_template % (line.name)
                errors.append(error_string)
        if errors:
            raise UserError(
                _("%s\n%s") % (_("No Taxes Defined!"), "\n".join(x for x in errors))
            )

        return super().action_confirm()
