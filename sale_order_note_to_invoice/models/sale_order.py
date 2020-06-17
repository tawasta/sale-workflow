from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_invoice_create(self, **kwargs):
        # Force line notes to invoice
        for order in self:
            for line in order.order_line:
                if line.display_type and line.display_type == "line_note":
                    # Set lines to be invoiced
                    # They will reset to 0 when "to invoice" compute triggers
                    line.qty_to_invoice = 1

        return super(SaleOrder, self).action_invoice_create(kwargs)
