import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):

    _inherit = "crm.lead"

    order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale order",
        compute="_compute_order_id",
        store=True,
    )

    order_line_ids = fields.One2many(
        related="order_id.order_line", string="Order lines"
    )

    pricelist_id = fields.Many2one(
        "product.pricelist", string="Pricelist", compute="_compute_pricelist_id"
    )

    @api.multi
    def action_set_lost(self):
        for record in self:
            for order in record.order_ids:
                if order.state in ["draft", "sent"]:
                    order.message_post(_("Opportunity lost"))
                    order.action_cancel()

        return super(CrmLead, self).action_set_lost()

    @api.multi
    def action_set_won(self):
        for record in self:
            for order in record.order_ids:
                if order.state in ["draft", "sent"]:
                    order.message_post(_("Opportunity won"))
                    order.action_confirm()

        return super(CrmLead, self).action_set_won()

    @api.depends("order_ids")
    def _compute_order_id(self):
        for record in self:
            if record.sale_number == 1:
                record.order_id = record.order_ids[0]
            else:
                record.order_id = False

    @api.multi
    def _compute_pricelist_id(self):
        for record in self:
            if record.sale_number == 1:
                record.pricelist_id = record.order_ids.filtered(
                    lambda r: r.state in ("draft", "sent")
                ).pricelist_id
