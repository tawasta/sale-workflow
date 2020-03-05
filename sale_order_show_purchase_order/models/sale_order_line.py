from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def _get_purchase_ids(self):

        group_list = []
        purchase_list = []

        purchases = self.purchase_order_ids.search([])

        for record in self.order_line:
            if record is not False:
                for line in self.order_line:
                    if line.procurement_ids.ids != []:
                        group_list.append(line.procurement_ids.group_id)

            if group_list != []:

                for group in group_list:
                    for id_number in group.procurement_ids:
                        if id_number.purchase_id and id_number.purchase_id.ids:
                            purchase_list.append(id_number.purchase_id.ids[0])

            if purchase_list != []:
                for i in purchase_list:
                    self.purchase_order_ids = [x for x in purchases.ids if x == i]

    purchase_order_ids = fields.Many2many(
        compute=_get_purchase_ids,
        comodel_name="purchase.order",
        string="Purchase Orders",
    )
