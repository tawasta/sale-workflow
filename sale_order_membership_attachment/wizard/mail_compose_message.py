from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields_list):
        res = super(MailComposeMessage, self).default_get(fields_list)
        if (
            res.get("res_id")
            and res.get("model")
            and res.get("composition_mode", "") != "mass_mail"
        ):
            res["can_attach_attachment"] = True

            if res.get("model") == "sale.order":
                sale_order = self.env["sale.order"].browse(res.get("res_id"))
                attachment_ids = sale_order.get_custom_attachment()
                if attachment_ids:
                    res["object_attachment_ids"] = [(6, 0, attachment_ids)]
        return res
