from odoo import _, api, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        picking = super().create(vals)

        # Yes, we search with origin-field which is not ideal
        origin = vals.get("origin")
        sale_id = self.env["sale.order"].sudo().search([("name", "=", origin)])

        if sale_id:
            # This is a link to a sale order
            ref = "<a href=# data-oe-model=sale.order data-oe-id=%d>%s</a>" % (
                sale_id.sudo().id,
                sale_id.sudo().name,
            )

            display_msg = """<div style="color: green;">
                Note by: {}
                </div>
                <div style="color: green;">
                This transfer has been created from: {}
                </div>
                """.format(
                sale_id.sudo().user_id.name, ref
            )

            picking.message_post(
                message_type="comment",
                subject=_("Sale Order created"),
                body=display_msg,
                notify_by_email=False,
                author_id=sale_id.sudo().user_id.partner_id.id,
            )

        return picking
