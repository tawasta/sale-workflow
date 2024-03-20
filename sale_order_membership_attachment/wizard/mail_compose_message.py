from odoo import api, models


class MailComposeMessage(models.TransientModel):

    _inherit = "mail.compose.message"

    def _is_attachment_autoselection_enabled(self):
        """
        If the found attachments should be checked by default, or if the user should
        check each manually. Defaults to true, expects no other attachments to be put
        on SOs.

        Can be overridden by adding the below config parameter and setting it to
        true.
        """
        return (
            not self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "sale_order_membership_attachment.bypass_attachment_autoselection",
                False,
            )
        )

    @api.model
    def default_get(self, fields_list):
        """
        Fetching the mail wizard view defaults
        """
        res = super(MailComposeMessage, self).default_get(fields_list)

        if (
            res.get("model") == "sale.order"
            and self._context.get("active_id")
            and res.get("composition_mode", "") != "mass_mail"
            and res["can_attach_attachment"]
            and self._is_attachment_autoselection_enabled()
        ):

            # The OCA module already lists all of the sale order's attachments in the
            # wizard, but this autochecks the selection boxes for all of them
            sale_order_attachment_ids = self.env["ir.attachment"].search(
                [
                    ("res_model", "=", "sale.order"),
                    ("res_id", "=", self._context.get("active_id")),
                ]
            )

            res["object_attachment_ids"] = [
                (6, 0, [a.id for a in sale_order_attachment_ids])
            ]

        return res
