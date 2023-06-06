import base64
import logging

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MailTemplate(models.Model):

    _inherit = "mail.template"

    def generate_email(self, res_ids, fields):
        """This is a core function from mail-module. It is modified to
        replace its attachements when using 'Sales Order: Send by email'
        email template"""
        mail = super().generate_email(res_ids, fields)

        # self._classify_per_lang(res_ids).items() returns for example
        # dict_items([('en_US', (mail.template(11,), [29]))])
        for _lang, (template, template_res_ids) in self._classify_per_lang(
            res_ids
        ).items():

            # Hardcoded condition to check if the used template is "Sales Order: Send by email"
            if template.id == self.env.ref("sale.mail_template_sale_confirmation").id:

                # Get template actions
                sale_template = self.env.ref("sale.action_report_saleorder")
                stock_template = self.env.ref(
                    "stock_report_title.action_report_delivery"
                )
                invoice_template = self.env.ref("account.account_invoices")

                # res_id is here the id value of a sale order. It is looped
                # just in case we try to send email from multiple sale orders.
                for res_id in template_res_ids:
                    attachments = []

                    sale = self.env["sale.order"].search([("id", "=", res_id)])
                    sale_report_name = sale and sale.name

                    if sale_template.report_type in ["qweb-html", "qweb-pdf"]:
                        result, _format = sale_template._render_qweb_pdf([res_id])
                    else:
                        res = sale_template._render([res_id])
                        if not res:
                            raise UserError(
                                _(
                                    "Unsupported report type %s found.",
                                    sale_template.report_type,
                                )
                            )
                        result, _format = res

                    result = base64.b64encode(result)
                    attachments.append((sale_report_name, result))

                    # Stock picking attachments
                    pickings = sale.picking_ids
                    for pick_id in pickings:
                        if stock_template.report_type in ["qweb-html", "qweb-pdf"]:
                            result, _format = stock_template._render_qweb_pdf(
                                [pick_id.id]
                            )
                        else:
                            res = stock_template._render([pick_id.id])
                            if not res:
                                raise UserError(
                                    _(
                                        "Unsupported report type %s found.",
                                        stock_template.report_type,
                                    )
                                )
                            result, _format = res

                        result = base64.b64encode(result)
                        attachments.append((pick_id.name, result))

                    # Invoice attachments
                    invoices = sale.invoice_ids
                    for inv_id in invoices:
                        if invoice_template.report_type in ["qweb-html", "qweb-pdf"]:
                            result, _format = invoice_template._render_qweb_pdf(
                                [inv_id.id]
                            )
                        else:
                            res = invoice_template._render([inv_id.id])
                            if not res:
                                raise UserError(
                                    _(
                                        "Unsupported report type %s found.",
                                        invoice_template.report_type,
                                    )
                                )
                            result, _format = res

                        result = base64.b64encode(result)
                        attachments.append((inv_id.name, result))

                    _logger.info("Email is being send with multiple attachments.")

                    # We replace the already created attachments to avoid duplicates
                    mail[res_id]["attachments"] = attachments
        return mail
