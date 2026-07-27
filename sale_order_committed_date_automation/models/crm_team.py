from odoo import _, api, exceptions, fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    delivery_date_weekdays = fields.Integer(
        string="Delivery lead time (weekdays)",
        default=False,
        help="Number of weekdays added to the delivery date. If empty, the "
        "company default is used.",
    )

    @api.constrains("delivery_date_weekdays")
    def _check_delivery_date_weekdays(self):
        for team in self:
            if team.delivery_date_weekdays and team.delivery_date_weekdays < 0:
                raise exceptions.ValidationError(
                    _("Delivery lead time (weekdays) must be a non-negative integer.")
                )
