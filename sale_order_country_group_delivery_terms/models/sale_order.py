from odoo import _, api, models
from odoo.tools import html2plaintext


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        self._add_delivery_term()

        return super(SaleOrder, self).action_confirm()

    def _add_delivery_term(self):
        for order in self:
            note_lines = html2plaintext(order.note).split("\n")

            delivery_info = (
                self.env["res.country.group"]
                .with_context(lang=order.partner_id.lang)
                .search([])
                .filtered(lambda r: r.delivery_terms)
                .mapped("delivery_terms")
            )

            note_lines = [
                line
                for line in note_lines
                if not any(word in line for word in delivery_info)
            ]

            note_lines = "<br>".join(note_lines)
            order.note = note_lines

            shipping_address = order.partner_shipping_id or order.partner_id
            country_groups = (
                shipping_address.country_id
                and shipping_address.country_id.country_group_ids
            ).filtered(lambda r: not r.skip_delivery_terms and r.delivery_terms)

            delivery_terms = []

            if country_groups:
                delivery_terms.append(
                    country_groups[0]
                    .with_context(lang=order.partner_id.lang)
                    .delivery_terms
                )

                msg = "<br>".join(delivery_terms)

                if msg:
                    order.note = "{}{}{}".format(
                        order.note, "<br>" if order.note else "", msg
                    )
