from odoo import _, models
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def action_sale_order_line_copy(self):
        """
        Copy an individual SO line. Checks config and places the line either
        a) directly after the copied line, or
        b) at the end or order
        """

        self.ensure_one()
        ir_config_model = self.env["ir.config_parameter"]
        lines = self.order_id.order_line

        if (
            ir_config_model.sudo().get_param(
                "sale_order_line_copy.sale_order_line_copy_mode"
            )
            == "directly_after"
        ):
            # Sort FIRST by sequence THEN by id
            sorted_lines = lines.sorted(key=lambda line: (line.sequence, line.id))

            # Big enough number is chosen because new lines have a default value of
            # 10 for their sequence.
            sequence = -1000

            # Index values start from 0. First element can have an index value of 0.
            self_index = sorted_lines.ids.index(self.id)

            for line in sorted_lines:
                line.sequence = sequence
                if sequence + 1000 == self_index:
                    sequence += 1
                    self.copy(
                        {
                            "order_id": self.order_id.id,
                            "sequence": sequence,
                        }
                    )
                sequence += 1
        else:
            max_seq_line = max(lines, key=lambda line: line.sequence)
            self.copy(
                {"order_id": self.order_id.id, "sequence": max_seq_line.sequence + 1}
            )

    def duplicate_section_and_contents(self):
        """
        Copy a whole section along with its individual SO lines. The copied section
        is always appended to the end of the Sale Order
        """

        self.ensure_one()

        lines = self.order_id.order_line

        # Get the biggest sequence in use so far, and increment by one
        max_seq_line = max(lines, key=lambda line: line.sequence)
        sequence_to_use = max_seq_line.sequence + 1

        # Duplicate the section line itself
        self.copy(
            {
                "order_id": self.order_id.id,
                "name": "%s (%s)" % (self.name, _("Copy")),
                "sequence": sequence_to_use,
            }
        )

        # Iterate through the individual SO lines that belong to that section
        sequence_to_use += 1
        for line in lines:
            if line.sequence < self.sequence or line.id == self.id:
                # Ignore everything before the section that is getting copied
                continue
            elif line.display_type == "line_section":
                # Stop iteration once we reach the next section
                break

            line.copy(
                {
                    "order_id": self.order_id.id,
                    "sequence": sequence_to_use,
                }
            )

            sequence_to_use += 1
