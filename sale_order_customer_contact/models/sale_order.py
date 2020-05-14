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
        "res.partner", "Contact", states=_FIELD_STATES
    )

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner(self):
        for record in self:
            if not record.partner_id:
                # Don't get a contact if there is no partner
                continue

            if record.partner_id != record.partner_id.commercial_partner_id:
                # Force commercial partner as partner
                record.partner_id = record.partner_id.commercial_partner_id

            if record.customer_contact_id.commercial_partner_id == \
                    record.partner_id:
                # Contact is already set
                continue

            customer_contact_id = record.partner_id.search(
                [
                    ("parent_id", "=", record.partner_id.id),
                    ("type", "=", "contact"),
                    ("is_company", "=", False),
                ],
                limit=1,
            )

            record.customer_contact_id = customer_contact_id

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

    @api.multi
    def create(self, values):
        if 'customer_contact_id' not in values:
            values['customer_contact_id'] = values['partner_id']

        res = super(SaleOrder, self).create(values)
        res.onchange_partner()

        return res

    @api.multi
    def write(self, values):
        if 'partner_id' in values:
            # Force using commercial partner as partner
            partner = self.env['res.partner'].browse(values['partner_id'])
            if partner.commercial_partner_id != partner:
                values['partner_id'] = partner.commercial_partner_id.id

        return super(SaleOrder, self).write(values)
