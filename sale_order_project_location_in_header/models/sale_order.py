from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    FIELD_STATES = {"draft": [("readonly", False)], "sent": [("readonly", False)]}

    stock_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Location",
        default=lambda self: self._default_get_stock_location(),
        states=FIELD_STATES,
        readonly=True,
        copy=False,
    )

    def _default_get_stock_location(self):
        if self.analytic_account_id and self.analytic_account_id.default_location_id:
            self.stock_location_id = self.analytic_account_id.default_location_id

    @api.onchange("analytic_account_id")
    @api.depends("analytic_account_id")
    def onchange_analytic_account_id_update_stock_location(self):
        for record in self:
            if (
                record.analytic_account_id
                and record.analytic_account_id.default_location_id
            ):
                record.stock_location_id = (
                    record.analytic_account_id.default_location_id.id
                )
