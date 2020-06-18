from odoo import fields, models, api
from datetime import datetime, timedelta
import logging

# Uncomment next line to enable debugging logging
# logging.basicConfig(level=100)


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _compute_commitment_date_from_week(self, week_number):
        """Return friday because friday is the best day"""
        days_in_week = 7
        nth_day = week_number * days_in_week - days_in_week
        current_year = datetime.now().year
        start_of_year = datetime(current_year, 1, 1, 0, 0)
        calculated_day = start_of_year + timedelta(days=nth_day, hours=12)
        increment = 1
        while calculated_day.strftime("%A") != "Friday":
            calculated_day = start_of_year \
                + timedelta(days=nth_day + increment, hours=12)
            increment = increment + 1
        return calculated_day

    def _default_week_of_shipment(self):
        current_week = datetime.today().isocalendar()[1]
        logging.log(100, "Current week: {0}".format(current_week))

        additional_weeks = 0
        if self.company_id.week_of_shipment_additional_weeks:
            additional_weeks = self.company_id.week_of_shipment_additional_weeks
        logging.log(100, "additional_weeks: {0}".format(additional_weeks))

        new_week = 0
        if additional_weeks > 0:
            new_week = current_week + additional_weeks
        else:
            new_week = current_week

        return new_week

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        default=_default_week_of_shipment,
        readonly=False,
    )

    def _ensure_proper_week(self, week):
        if week < 0:
            return 0
        elif week > 52:
            return 52
        else:
            return week

    @api.depends("week_of_shipment")
    @api.onchange("week_of_shipment")
    def _compute_week_of_shipment(self):
        current_week = datetime.today().isocalendar()[1]
        logging.log(100, "Current week: {0}".format(current_week))

        additional_weeks = 0
        apply_additional_week_rule = self.env.user\
            in self.company_id.week_of_shipment_additional_weeks_group.users

        if not self.company_id.week_of_shipment_additional_weeks_group:
            # If no group is set then rules apply to everybody
            apply_additional_week_rule = True

        if self.company_id.week_of_shipment_additional_weeks:
            additional_weeks = self.company_id.week_of_shipment_additional_weeks

        logging.log(100, "Apply additional week rule: {0}"
                    .format(apply_additional_week_rule))

        for record in self:
            logging.log(100, record.week_of_shipment)
            if record.week_of_shipment:
                new_week = self._ensure_proper_week(record.week_of_shipment)
                if apply_additional_week_rule:
                    if new_week <= current_week + additional_weeks:
                        new_week = current_week + additional_weeks
                record.week_of_shipment = new_week
                record.commitment_date = \
                    self._compute_commitment_date_from_week(new_week)
