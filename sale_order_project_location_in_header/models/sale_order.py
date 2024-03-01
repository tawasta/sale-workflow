from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    stock_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Location",
        default=lambda self: self._default_get_stock_location(),
        copy=False,
    )

    def _default_get_stock_location(self):
        if self.analytic_account_id and self.analytic_account_id.default_location_id:
            self.stock_location_id = self.analytic_account_id.default_location_id

    @api.onchange("analytic_account_id")
    def onchange_analytic_account_id_update_stock_location(self):
        account_id = self.analytic_account_id
        self.stock_location_id = account_id and account_id.default_location_id or False

    def action_confirm(self):
        res = super().action_confirm()
        for sale in self:
            picking_values = {"location_id": sale.stock_location_id}
            sale.picking_ids.write(picking_values)
        return res
