import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailComposeMessage(models.TransientModel):

    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields_list):
        """
        Override the default suggested "Sales order: send by email" template and
        suggest the SO confirmation template instead
        """
        res = super(MailComposeMessage, self).default_get(fields_list)

        if (
            res.get("model") == "sale.order"
            and self._context.get("active_id")
            and res.get("composition_mode", "") != "mass_mail"
        ):
            res["template_id"] = (
                self.env["sale.order"]
                .browse(self._context.get("active_id"))
                ._find_mail_template(force_confirmation_template=True)
            )

        return res
