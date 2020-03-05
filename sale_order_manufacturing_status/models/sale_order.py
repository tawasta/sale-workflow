from odoo import api, fields, models


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields
    mrp_production_ids = fields.Many2many(
        comodel_name="mrp.production",
        compute="_compute_mrp_production_ids",
        string="Manufacturing Orders",
    )

    manufacturing_status = fields.Selection(
        selection=[
            ("none", "Nothing to Manufacture"),
            ("open", "To Manufacture"),
            ("exception", "Manufacturing Exception"),
            ("done", "Fully Manufactured"),
        ],
        compute="_compute_manufacturing_status",
        string="Manufacturing Status",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.multi
    def _compute_mrp_production_ids(self):
        """ Find all manufacturing orders that belong to the Sale Order's
        procurement group """

        for sale in self:
            mrp_production_model = self.env["mrp.production"]

            if sale.procurement_group_id:
                args = [("procurement_group_id", "=", sale.procurement_group_id.id)]

                # Search with sudo() so that also salesmen can see the status
                manufacturing_orders = mrp_production_model.sudo().search(args=args)
            else:
                manufacturing_orders = []

            sale.mrp_production_ids = [mo.id for mo in manufacturing_orders]

    @api.multi
    def _compute_manufacturing_status(self):
        """ Set the status based on the individual MO states
        - Nothing to Manufacture: no MOs linked to the SO
        - Manufacturing Exception: any MOs are in Cancel state
        - Fully Manufactured: all MOs are in Done state
        - To Manufacture: some MOs are unfinished """

        for sale in self:
            if not sale.mrp_production_ids:
                sale.manufacturing_status = "none"
            else:
                if all([mo.state == "done" for mo in sale.mrp_production_ids]):
                    sale.manufacturing_status = "done"
                elif any([mo.state == "cancel" for mo in sale.mrp_production_ids]):
                    sale.manufacturing_status = "exception"
                else:
                    sale.manufacturing_status = "open"

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
