from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_custom_attachment(self):
        existing_attachments = self.env["ir.attachment"].search(
            [("res_model", "=", "sale.order"), ("res_id", "=", self.id)]
        )
        existing_checksums = [att.checksum for att in existing_attachments]
        new_attachments = []
        for line in self.order_line:
            if line.product_id.membership:
                for attachment in line.product_id.membership_attachment_ids:
                    if attachment.checksum not in existing_checksums:
                        new_attachment = attachment.copy(
                            {"res_model": "sale.order", "res_id": self.id}
                        )
                        new_attachments.append(new_attachment)
                        existing_checksums.append(attachment.checksum)

        return [att.id for att in existing_attachments] + [
            new_att.id for new_att in new_attachments
        ]
