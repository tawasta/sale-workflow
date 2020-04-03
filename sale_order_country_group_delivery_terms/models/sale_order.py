from odoo import _, api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        self._add_delivery_term()

        return super(SaleOrder, self).action_confirm()

    def _add_delivery_term(self):
        for record in self:
            shipping_address = record.partner_shipping_id or record.partner_id

            country_groups = (
                shipping_address.country_id
                and shipping_address.country_id.country_group_ids
            ).filtered(lambda r: not r.skip_delivery_terms)

            country_groups = [x for x in country_groups if x.delivery_terms]

            if country_groups:
                delivery_terms = country_groups[0].delivery_terms
                msg = "{}: {}".format(_("Delivery terms"), delivery_terms)

                if record.note:
                    record.note += "\n%s" % msg
                else:
                    record.note = msg
