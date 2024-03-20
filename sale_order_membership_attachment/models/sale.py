from odoo import _, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        """
        Handle the attachment copying when SO is confirmed
        """
        res = super(SaleOrder, self).action_confirm()
        self.copy_membership_attachments_from_product()
        return res

    def copy_membership_attachments_from_product(self):
        """
        Copy any membership product attachments from product to sale order, so they're
        ready to be added to mail wizard by OCA's mail_attach_existing_attachment
        """

        for sale_order in self:

            existing_attachments = self.env["ir.attachment"].search(
                [("res_model", "=", "sale.order"), ("res_id", "=", sale_order.id)]
            )
            existing_checksums = [att.checksum for att in existing_attachments]

            for line in sale_order.order_line:
                if line.product_id.membership:
                    for attachment in line.product_id.membership_attachment_ids:
                        # Avoid adding same attachment twice
                        if attachment.checksum not in existing_checksums:
                            attachment.copy(
                                {"res_model": "sale.order", "res_id": sale_order.id}
                            )
                            # Log a note to chatter
                            msg = _(
                                "Fetched membership product attachment '%s' "
                                "from Product to Sale Order",
                                attachment.name,
                            )

                            sale_order.message_post(body=msg)
                            existing_checksums.append(attachment.checksum)
