from odoo import api, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            note_lines = self.note.split('\n')
            tax_info = self.env['account.tax'].search([]).filtered(
                lambda tx: tx.sale_order_note).mapped('sale_order_note')

            note_lines = [line for line in note_lines \
                    if not any(word in line for word in tax_info)]

            note_lines = '\n'.join(note_lines)
            order.note = note_lines

            tax_info = []

            if order.order_line:
                for line in order.order_line:
                    tax_note = line.tax_id.sale_order_note
                    if tax_note and tax_note not in tax_info:
                        tax_info.append(tax_note)

            tax_info = '\n'.join(tax_info)

            if tax_info:
                order.note = '{}{}{}'.format(note_lines,
                    '\n' if note_lines else '', tax_info)
        return res
