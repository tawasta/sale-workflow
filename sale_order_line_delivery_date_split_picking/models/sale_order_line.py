from datetime import datetime, time, timedelta

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Date("Delivery Date")
    procurement_group_id = fields.Many2one(
        "procurement.group", "Procurement Group", copy=False
    )

    def _prepare_procurement_values(self, group_id=False):
        vals = super()._prepare_procurement_values(group_id)

        if self.commitment_date:
            commitment_date = datetime.combine(self.commitment_date, time(12))
            planned = commitment_date - timedelta(
                days=self.order_id.company_id.security_lead
            )

            vals.update({"date_planned": planned, "date_deadline": commitment_date})
        return vals

    def _get_procurement_group(self):
        # Split one SO into different procurement groups,
        # if there are multiple commitment dates

        # Calling super to run any logic done there,
        # even when we don't use the result
        super()._get_procurement_group()

        # Try to find order lines with same commitment date
        order_lines = self.order_id.order_line.filtered(
            lambda sale_line: sale_line.commitment_date == self.commitment_date
            and sale_line.procurement_group_id
        )

        if order_lines:
            # Use existing procurement group
            group_id = order_lines[0].procurement_group_id
        else:
            # Create a new procurement group
            group_id = self.env["procurement.group"].create(
                self._prepare_procurement_group_vals()
            )
        self.procurement_group_id = group_id

        return group_id
