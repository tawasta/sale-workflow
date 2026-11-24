from odoo import api, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.constrains("is_optional")
    def _check_is_optional_on_quotation(self):
        # An optional section is left out of the total, which must not change on
        # a confirmed order.
        for line in self.filtered("is_optional"):
            if line.order_id.state not in ("draft", "sent"):
                raise ValidationError(
                    self.env._("A section can be optional only on a quotation.")
                )

    def _get_section_totals(self, totals_field):
        # The lines of an optional subsection are left out of the total of a regular
        # section, as they are left out of the order total.
        if self.display_type != "line_section" or self.is_optional:
            return super()._get_section_totals(totals_field)
        section_lines = self._get_section_lines() - self.order_id._get_optional_lines()
        return sum(section_lines.mapped(totals_field))

    def _is_order_level_line(self):
        """Return whether the line concerns the whole order. Sale adds these lines
        at the end of the order, so they would otherwise fall in the last section."""
        self.ensure_one()
        return self.is_downpayment or self._is_delivery() or self._is_global_discount()
