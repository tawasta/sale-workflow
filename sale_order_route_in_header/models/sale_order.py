from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    route_id = fields.Many2one(
        comodel_name="stock.location.route",
        string="Route",
        domain=[("sale_selectable", "=", True)],
        check_company=True,
    )

    @api.onchange("route_id")
    def onchange_route_id(self):
        for record in self:
            for line in record.order_line:
                line.route_id = record.route_id
