import base64
import io

from odoo import models
from odoo.tools.pdf import PdfFileWriter


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        result = super()._render_qweb_pdf_prepare_streams(
            report_ref, data, res_ids=res_ids
        )
        if self._get_report(report_ref).report_name != "sale.report_saleorder":
            return result

        orders = self.env["sale.order"].browse(res_ids)

        for order in orders:
            initial_stream = result[order.id]["stream"]
            if initial_stream:
                header_record = order.sale_header_document_id
                footer_record = order.sale_footer_document_id
                has_header = bool(order.sale_header_document_id)
                has_footer = bool(order.sale_footer_document_id)

                if (
                    not has_header
                    and not (header_record or footer_record)
                    and not has_footer
                ):
                    continue

                writer = PdfFileWriter()
                if header_record:
                    self._add_pages_to_writer(
                        writer, base64.b64decode(header_record.datas)
                    )
                self._add_pages_to_writer(writer, initial_stream.getvalue())
                if footer_record:
                    self._add_pages_to_writer(
                        writer, base64.b64decode(footer_record.datas)
                    )

                with io.BytesIO() as _buffer:
                    writer.write(_buffer)
                    stream = io.BytesIO(_buffer.getvalue())
                result[order.id].update({"stream": stream})

        return result
