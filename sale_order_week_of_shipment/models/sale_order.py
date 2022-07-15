from odoo import fields, models, api
from datetime import datetime
from isoweek import Week
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _compute_commitment_date_from_week(self, week_number):
        """ Return friday because friday is the best day """

        year, week, day = datetime.now().isocalendar()
        if week_number < week:
            # If the week number is smaller than current week number,
            # jump to the next year
            year += 1

        #         week_string = "{}-{}-{}".format(year, week_number, 5)
        #         calculated_day = datetime.strptime(week_string, "%G-%V-%u")

        # Temporary fix
        iso_week = Week(year, week_number).day(4)
        calculated_day_iso = iso_week.strftime("%Y-%m-%d 00:00:00")

        return calculated_day_iso

    def _default_week_of_shipment(self):
        current_week = datetime.today().isocalendar()[1]
        _logger.debug("Current week: {0}".format(current_week))

        additional_weeks = 0
        if self.company_id.week_of_shipment_additional_weeks:
            additional_weeks = self.company_id.week_of_shipment_additional_weeks
        _logger.debug("additional_weeks: {0}".format(additional_weeks))

        if additional_weeks > 0:
            new_week = current_week + additional_weeks
        else:
            new_week = current_week

        return new_week

    week_of_shipment = fields.Integer(
        string="Week of shipment", default=lambda self: self._default_week_of_shipment(), readonly=False,
    )

    def _ensure_proper_week(self, week):
        if week < 0:
            return 0
        elif week > 53:
            return 53
        else:
            return week

    @api.depends("week_of_shipment")
    @api.onchange("week_of_shipment")
    def _compute_week_of_shipment(self):
        current_week = datetime.today().isocalendar()[1]
        _logger.debug("Current week: {0}".format(current_week))

        additional_weeks = 0
        apply_additional_week_rule = (
            self.env.user
            in self.company_id.week_of_shipment_additional_weeks_group.users
        )

        if not self.company_id.week_of_shipment_additional_weeks_group:
            # If no group is set then rules apply to everybody
            apply_additional_week_rule = True

        if (
            self.company_id.week_of_shipment_additional_weeks
            and apply_additional_week_rule
        ):
            additional_weeks = self.company_id.week_of_shipment_additional_weeks

        _logger.debug(
            "Apply additional week rule: {0}".format(apply_additional_week_rule)
        )

        for record in self:
            _logger.debug(
                "Requested week of shipment {0}".format(record.week_of_shipment)
            )
            if not record.week_of_shipment:
                continue

            # Requested week
            new_week = self._ensure_proper_week(record.week_of_shipment)
            # First possible week
            possible_week = current_week + additional_weeks

            # Requested commitment date
            commitment_date = self._compute_commitment_date_from_week(new_week)
            # First possible commitment date
            possible_commitment_date = self._compute_commitment_date_from_week(
                current_week + additional_weeks
            )
            # Postpone commitment date, if requested is not possible
            if commitment_date < possible_commitment_date:
                commitment_date = possible_commitment_date
                new_week = possible_week

            record.week_of_shipment = new_week
            record.commitment_date = commitment_date
