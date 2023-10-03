from odoo import models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def action_immediate_transfer_wizard(self):
        wiz = (
            self.env["stock.immediate.transfer"]
            .with_context(button_validate_picking_ids=self.ids)
            .create(
                {
                    "pick_ids": [(4, p.id) for p in self],
                }
            )
        )

        lines = self.env["stock.immediate.transfer.line"]

        for pick in self:
            lines += self.env["stock.immediate.transfer.line"].create(
                {
                    "immediate_transfer_id": wiz.id,
                    "picking_id": pick.id,
                    "to_immediate": True,
                }
            )
            pick = pick.with_context(button_validate_picking_ids=pick.id)

        wiz.immediate_transfer_line_ids = lines
        wiz.with_context({"button_validate_picking_ids": self.ids})
        wiz.process()
