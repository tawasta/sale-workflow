from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    delivery_info = fields.Text(string="Deliveries", compute="_compute_delivery_info")

    @api.multi
    def _compute_delivery_info(self):
        # Computes the deliveries on sale order lines,
        # based on done stock moves related to its procurements

        for record in self:
            delivery_info = ""

            moves = record.move_ids.filtered(
                lambda r: r.state == "done" and not r.scrapped
            ).sorted(key=lambda r: r.picking_id.date_done)

            for move in moves:

                qty = move.product_uom._compute_quantity(
                    move.product_uom_qty, record.product_uom
                )

                picking = move.picking_id

                if move.location_dest_id.usage == "customer":
                    if not move.origin_returned_move_id:
                        # Nothing to do here
                        pass

                elif move.location_dest_id.usage != "customer":
                    delivery_info += "-"

                delivery_info += "{} {} / {} \n".format(
                    qty, move.product_uom.name, picking.date_done
                )

            record.delivery_info = delivery_info
