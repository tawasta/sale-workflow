from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def print_receipt(self):
        receipt = self.env.ref("account.action_report_payment_receipt")
        return receipt.report_action(self.reconciled_payment_ids.ids, config=False)
