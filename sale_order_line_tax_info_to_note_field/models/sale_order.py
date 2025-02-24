from odoo import api, models
from odoo.tools import html2plaintext


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            note_lines = html2plaintext(order.note).split("\n")
            tax_info = (
                self.env["account.tax"]
                .with_context(lang=order.partner_id.lang)
                .search([])
                .filtered(lambda tx: tx.sale_order_note)
                .mapped("sale_order_note")
            )

            note_lines = [
                line
                for line in note_lines
                if not any(word in line for word in tax_info)
            ]

            note_lines = "<br>".join(note_lines)
            order.note = note_lines

            tax_info = []

            for line in order.order_line:
                tax_note = line.with_context(
                    lang=order.partner_id.lang
                ).tax_id.sale_order_note
                if tax_note and tax_note not in tax_info:
                    tax_info.append(tax_note)

            tax_info = "<br>".join(tax_info)

            if tax_info:
                order.note = "{}{}{}".format(
                    note_lines, "<br>" if note_lines else "", tax_info
                )
        return res
