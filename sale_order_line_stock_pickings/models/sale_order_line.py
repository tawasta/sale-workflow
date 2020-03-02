# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class SaleOrderLine(models.Model):

    # 1. Private attributes
    _inherit = "sale.order.line"

    # 2. Fields declaration
    delivery_info = fields.Text(string="Deliveries", compute="_compute_delivery_info")

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.multi
    def _compute_delivery_info(self):
        # Computes the deliveries on sale order lines,
        # based on done stock moves related to its procurements

        for record in self:
            delivery_info = ""

            procurements = (
                record.procurement_ids.mapped("move_ids")
                .filtered(lambda r: r.state == "done" and not r.scrapped)
                .sorted(key=lambda r: r.picking_id.date_done)
            )

            for move in procurements:

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

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
