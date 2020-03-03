from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    _FIELD_STATES = {
        "draft": [("readonly", False)],
        "sent": [("readonly", False)],
        "manual": [("readonly", False)],
    }

    # TODO: change the field name to partner_contact_id when migrating
    customer_contact_id = fields.Many2one(
        "res.partner",
        "Contact",
        states=_FIELD_STATES
    )

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner(self):
        self.ensure_one()

        # Don't get a contact if there is no partner
        if not self.partner_id:
            return False

        # Contact is already set
        if self.customer_contact_id.parent_id == self.partner_id:
            return False

        self.customer_contact_id = self.partner_id.search(
            [
                ("parent_id", "=", self.partner_id.id),
                ("type", "=", "contact"),
                ("is_company", "=", False),
            ],
            limit=1,
        )

    @api.multi
    @api.onchange("partner_id")
    @api.depends("customer_contact_id")
    def onchange_partner_domain_change(self):
        # Get the contact domain
        res = dict()
        if self.partner_id:
            contacts = self.env["res.partner"].search(
                [
                    ("commercial_partner_id", "=", self.partner_id.id),
                    ("type", "=", "contact"),
                    ("is_company", "=", False),
                ]
            )

            if contacts:
                domain = [("id", "in", contacts.ids)]
                res["domain"] = {"customer_contact_id": domain}

        return res

    @api.multi
    def _prepare_invoice(self):
        # Handling for when invoicing the invoiceable lines
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals["customer_contact_id"] = (
            self.customer_contact_id and self.customer_contact_id.id or False
        )
        return invoice_vals
