import pytz

from odoo import _, api, exceptions, fields, models


def _tz_get():
    # Getting timezones from pytz module instead of using the database table
    return [
        (tz, tz)
        for tz in sorted(
            pytz.all_timezones, key=lambda tz: tz if not tz.startswith("Etc/") else "_"
        )
    ]


class ResCompany(models.Model):
    _inherit = "res.company"

    delivery_date_automation = fields.Selection(
        selection=[
            ("no", "No automation"),
            ("company", "Company-wide"),
            ("team", "Sales team specific"),
        ],
        string="Delivery date automation",
        default="no",
        required=True,
    )
    delivery_date_timezone = fields.Selection(
        selection=_tz_get(),
        string="Delivery date timezone",
        default=lambda self: self.env.user.tz or "UTC",
    )
    delivery_date_time_cutoff = fields.Float(
        string="Delivery date time cutoff",
        default=12.0,
        help="Confirmation before this time counts the current day as day 0. "
        "Confirmation at or after this time counts the current day as day 1.",
    )
    delivery_date_default_weekdays = fields.Integer(
        string="Default delivery lead time (weekdays)",
        default=False,
        help="Number of weekdays added to the delivery date. Used in "
        "company-wide mode and as fallback for sales teams.",
    )

    @api.constrains("delivery_date_time_cutoff")
    def _check_delivery_date_time_cutoff(self):
        for company in self:
            if (
                company.delivery_date_time_cutoff < 0
                or company.delivery_date_time_cutoff >= 24
            ):
                raise exceptions.ValidationError(
                    _("Delivery date time cutoff must be between 00:00 and 23:59.")
                )

    @api.constrains("delivery_date_default_weekdays")
    def _check_delivery_date_default_weekdays(self):
        for company in self:
            if company.delivery_date_default_weekdays < 0:
                raise exceptions.ValidationError(
                    _(
                        "Default delivery lead time (weekdays) must be a "
                        "non-negative integer."
                    )
                )
