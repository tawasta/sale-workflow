import base64
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_header_document_id = fields.Many2one(
        "ir.attachment", string="PDF header document", copy=False
    )
    sale_footer_document_id = fields.Many2one(
        "ir.attachment", string="PDF footer document", copy=False
    )

    @api.constrains("sale_header_document_id", "sale_footer_document_id")
    def _check_datas_compatibility(self):
        for sale in self:
            if (
                sale.sale_header_document_id.datas
                and not sale.sale_header_document_id.mimetype.endswith("pdf")
            ) or (
                sale.sale_footer_document_id.datas
                and not sale.sale_footer_document_id.mimetype.endswith("pdf")
            ):
                raise ValidationError(
                    _("Only PDF documents can be attached inside a quote.")
                )
