from odoo import api
from odoo import models
from odoo.exceptions import UserError


class AccountMoveSend(models.TransientModel):
    _inherit = "account.move.send"

    @api.depends("move_ids")
    def _compute_company_id(self):
        try:
            super()._compute_company_id()
        except UserError:
            # Override "You can only send from the same company"-error
            pass
