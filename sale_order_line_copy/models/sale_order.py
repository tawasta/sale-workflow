from odoo import _, models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_duplicate_section_wizard(self):
        """Open the wizard to duplicate a section"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Duplicate a Section",
            "res_model": "sale_order_line_copy.section_duplicate_wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_order_id": self.id,
            },
        }
