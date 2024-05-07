from odoo import _, exceptions, models


class SaleAdvancePaymentInv(models.TransientModel):

    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        ir_config_model = self.env["ir.config_parameter"]

        if not ir_config_model.sudo().get_param("sale_bypass_tags_required"):
            sale_orders = self.env["sale.order"].browse(
                self._context.get("active_ids", [])
            )
            for order in sale_orders:
                lines = order.order_line.filtered(lambda l: not l.display_type)
                for line in lines:
                    if not line.analytic_tag_ids:
                        msg = (
                            _("The line with a product %s requires a tag")
                            % line.product_id.name
                        )
                        raise exceptions.UserError(msg)

        return super().create_invoices()
