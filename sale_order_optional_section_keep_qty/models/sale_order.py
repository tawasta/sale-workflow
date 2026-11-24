from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # The sequence decides which section a line belongs to.
    @api.depends("order_line.is_optional", "order_line.sequence")
    def _compute_amounts(self):
        return super()._compute_amounts()

    @api.depends("order_line.is_optional", "order_line.sequence")
    def _compute_tax_totals(self):
        return super()._compute_tax_totals()

    @api.depends("order_line.is_optional", "order_line.sequence")
    def _compute_margin(self):
        res = super()._compute_margin()
        for order in self:
            optional_lines = order._get_optional_lines()
            if not optional_lines:
                continue
            order.margin -= sum(optional_lines.mapped("margin"))
            order.margin_percent = (
                order.amount_untaxed and order.margin / order.amount_untaxed
            )
        return res

    def _compute_amount_undiscounted(self):
        # Otherwise the portal shows the optional lines as a saving of the customer.
        res = super()._compute_amount_undiscounted()
        AccountTax = self.env["account.tax"]
        for order in self:
            for line in order._get_optional_lines():
                base_line = line._prepare_base_line_for_taxes_computation(discount=0)
                AccountTax._add_tax_details_in_base_line(base_line, order.company_id)
                order.amount_undiscounted -= base_line["tax_details"][
                    "raw_total_excluded_currency"
                ]
        return res

    def _get_priced_lines(self):
        optional_lines = self.env["sale.order.line"].concat(
            *(order._get_optional_lines() for order in self)
        )
        return super()._get_priced_lines() - optional_lines

    def _confirmation_error_message(self):
        error_message = super()._confirmation_error_message()
        if error_message or not self._has_optional_section():
            return error_message
        # Also shown to the customer who accepts the quotation in the portal.
        return self.env._(
            "The quotation has optional sections. Before the order is confirmed, "
            "the salesperson deletes them or sets the section the customer chose "
            "as a regular section."
        )

    def _can_be_edited_on_portal(self):
        # The customer tells the choice to the salesperson instead of changing the
        # quantities of the optional lines in the portal.
        return False

    def _has_optional_section(self):
        self.ensure_one()
        return any(self.order_line.mapped("is_optional"))

    def _get_optional_lines(self):
        """Return the product lines of the optional sections and subsections. The
        sections are read from the line order, as the cached parent section of a
        line is not recomputed when the lines are resequenced."""
        self.ensure_one()
        optional_lines = []
        in_optional_section = in_optional_subsection = False
        for line in self.order_line.sorted("sequence"):
            if line.display_type == "line_section":
                in_optional_section = line.is_optional
                in_optional_subsection = False
            elif line.display_type == "line_subsection":
                in_optional_subsection = line.is_optional
            elif (
                (in_optional_section or in_optional_subsection)
                and not line.display_type
                and not line._is_order_level_line()
            ):
                optional_lines.append(line)
        return self.env["sale.order.line"].concat(*optional_lines)
