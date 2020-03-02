from odoo import _, exceptions, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def check_missing_partner_fields(self):
        missing_fields = []
        for field in self.company_id.mandatory_partner_field_ids:
            if not self.partner_id[field.name]:
                missing_fields.append(field.field_description)

        return missing_fields

    def action_confirm(self):
        missing_partner_fields = self.check_missing_partner_fields()
        if missing_partner_fields:
            msg = _("Please fill in the following fields for the customer: ")
            msg += ", ".join(missing_partner_fields)
            raise exceptions.UserError(msg)

        return super(SaleOrder, self).action_confirm()
