from odoo import _, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_confirm(self):
        """Add name (order reference), salesperson and notice period to sale note"""
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            if order.name:
                reference = _("Our reference: %s") % order.name

                if order.note:
                    order.note = reference + "\n" + order.note
                else:
                    order.note = reference

            if order.user_id:
                salesperson = _("Salesperson: %s") % order.user_id.name

                if order.note:
                    order.note = salesperson + "\n" + order.note
                else:
                    order.note = salesperson

            notice_period_days = (
                self.partner_id.notice_period or self.company_id.notice_period
            )
            notice_period = _("Notice period: %s days") % notice_period_days

            if order.note:
                order.note = notice_period + "\n" + order.note
            else:
                order.note = notice_period
        return res

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()

        if self.note:
            note_lines = self.note.split("\n")

            words_to_remove = [
                _("Salesperson:"),
                _("Notice period:"),
                _("Our reference:"),
            ]

            note_lines = [
                line
                for line in note_lines
                if not any(word in line for word in words_to_remove)
            ]

            note_lines = "\n".join(note_lines)

            self.note = note_lines
        return res
