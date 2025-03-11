from odoo import api, models
from odoo.tools import is_html_empty


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _compute_note(self):
        # Disable note compute when partner is changed
        return

    @api.onchange("sale_order_template_id")
    @api.depends("sale_order_template_id")
    def _compute_note_from_sale_order_template(self):
        # A new trigger to force note recompute when changing template
        for order in self.filtered("sale_order_template_id"):
            template = order.sale_order_template_id.with_context(
                lang=order.partner_id.lang
            )
            order.note = (
                template.note if not is_html_empty(template.note) else order.note
            )
