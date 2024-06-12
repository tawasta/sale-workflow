import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def _onchange_product_id_set_customer_lead(self):
        """
        Override sale_stock's lead time calculation to be based on resource calendar,
        if one is defined for the warehouse
        """

        if self.order_id.company_id.sale_lead_time_resource_calendar_id:

            today = fields.Datetime.now().replace(hour=23, minute=59, second=59)

            # - compute_leaves=True takes into account any global holidays in the
            #   resource calendar, and adds extra days to lead time accordingly
            resource_based_date = (
                self.order_id.company_id.sale_lead_time_resource_calendar_id.plan_days(
                    days=self.product_id.sale_delay,
                    day_dt=today,
                    compute_leaves=True,
                )
            )

            # - incremented by +1 to not take current day into consideration
            resource_based_day_diff = (resource_based_date - today).days + 1
            self.customer_lead = resource_based_day_diff
        else:
            # If no resource calendar is defined, fall back to default lead time
            # calculation
            return super()._onchange_product_id_set_customer_lead()
