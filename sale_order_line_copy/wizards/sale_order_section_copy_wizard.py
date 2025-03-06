from odoo import _, models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrderSectionDuplicateWizard(models.TransientModel):
    _name = "sale_order_line_copy.section_duplicate_wizard"
    _description = "Duplicate Sale Order Section Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", required=True)

    section_line_id = fields.Many2one(
        "sale.order.line",
        string="Section to Duplicate",
        domain="[('order_id', '=', sale_order_id), ('display_type', '=', 'line_section')]",
        required=True,
    )

    @api.model
    def default_get(self, fields):
        """Initialize the wizard fields using the SO from which wizard was reached"""

        res = super().default_get(fields)
        if self.env.context.get("active_id"):
            res["sale_order_id"] = self.env.context["active_id"]

        return res

    def action_duplicate_section(self):
        """Duplicate the selected section"""

        self.section_line_id.duplicate_section_and_contents()
