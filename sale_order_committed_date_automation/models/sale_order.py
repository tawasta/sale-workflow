import logging
from datetime import datetime, timedelta

import pytz

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.commitment_date:
                continue
            automation = order.company_id.delivery_date_automation
            if automation == "no":
                continue
            order.commitment_date = order._compute_delivery_date(automation)
        return res

    def _compute_delivery_date(self, automation):
        """Return the UTC datetime to store in the commitment_date field."""
        self.ensure_one()
        company = self.company_id
        tz_name = company.delivery_date_timezone or "UTC"
        tz = pytz.timezone(tz_name)

        confirmation_dt = self.date_order or fields.Datetime.now()
        localized = pytz.utc.localize(confirmation_dt).astimezone(tz)

        current_date = localized.date()
        cutoff = company.delivery_date_time_cutoff or 0.0
        cutoff_time = (datetime.min + timedelta(hours=cutoff)).time()
        after_cutoff = localized.time() >= cutoff_time

        start_date = self._get_delivery_start_date(current_date, after_cutoff)
        weekdays = self._get_delivery_weekdays(automation)
        result_date = self._add_weekdays(start_date, weekdays)

        result_dt = datetime.combine(result_date, datetime.min.time())
        aware_local = tz.localize(result_dt)
        return aware_local.astimezone(pytz.utc).replace(tzinfo=None)

    def _get_delivery_start_date(self, current_date, after_cutoff):
        self.ensure_one()
        if current_date.weekday() >= 5:
            return self._add_weekdays(current_date, 1)
        if after_cutoff:
            return self._add_weekdays(current_date, 1)
        return current_date

    def _get_delivery_weekdays(self, automation):
        self.ensure_one()
        if automation == "team":
            return (
                self.team_id.delivery_date_weekdays
                or self.company_id.delivery_date_default_weekdays
                or 0
            )
        return self.company_id.delivery_date_default_weekdays or 0

    def _add_weekdays(self, start_date, weekdays):
        self.ensure_one()
        if weekdays <= 0:
            if start_date.weekday() >= 5:
                return start_date + timedelta(days=7 - start_date.weekday())
            return start_date

        result = start_date
        for _ in range(weekdays):
            result += timedelta(days=1)
            while result.weekday() >= 5:
                result += timedelta(days=1)
        return result
