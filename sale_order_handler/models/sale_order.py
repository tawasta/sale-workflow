from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    handler = fields.Many2one(
        "res.partner",
        string="Handler",
    )

    def action_confirm(self):
        res = super().action_confirm()

        for pick in self.picking_ids:
            pick.write(
                {
                    "handler": self.handler.id,
                }
            )

        return res

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()
        if self.handler:
            invoice_vals["handler"] = self.handler

        return invoice_vals
