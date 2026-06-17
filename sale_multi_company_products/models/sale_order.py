from odoo import fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    current_invoice_company_id = fields.Many2one(
        string="Current company to invoice",
        help="Technical field used while splitting invoices by product variant company.",
        comodel_name="res.company",
        readonly=True,
        copy=False,
    )

    def _check_order_line_company_id(self):
        return

    def _get_variant_company_invoiceable_lines(self, final=False):
        self.ensure_one()
        return super(SaleOrder, self)._get_invoiceable_lines(final=final).filtered(
            lambda line: (
                not line.display_type
                and line.product_id
                and line.product_id.variant_company_id
            )
        )

    def _get_neutral_invoiceable_lines(self, final=False):
        self.ensure_one()
        return super(SaleOrder, self)._get_invoiceable_lines(final=final).filtered(
            lambda line: (
                line.display_type
                or not line.product_id
                or not line.product_id.variant_company_id
            )
        )

    def _get_invoiceable_lines(self, final=False):
        lines = super()._get_invoiceable_lines(final=final)

        if not self.current_invoice_company_id:
            return lines

        variant_lines = lines.filtered(
            lambda line: (
                not line.display_type
                and line.product_id
                and line.product_id.variant_company_id == self.current_invoice_company_id
            )
        )

        neutral_lines = lines.filtered(
            lambda line: (
                line.display_type
                or not line.product_id
                or not line.product_id.variant_company_id
            )
        )

        companies = self._get_variant_company_invoiceable_lines(final=final).mapped(
            "product_id.variant_company_id"
        )
        first_company = companies[:1]

        if self.current_invoice_company_id == first_company:
            return variant_lines | neutral_lines

        return variant_lines

    def _get_split_invoice_companies(self, final=False):
        self.ensure_one()

        companies = self._get_variant_company_invoiceable_lines(final=final).mapped(
            "product_id.variant_company_id"
        )

        if companies:
            return companies

        return self.company_id

    def _validate_split_invoice_partners(self):
        self.ensure_one()

        partners = self.partner_id | self.partner_invoice_id | self.partner_shipping_id
        bad_partners = partners.filtered(lambda partner: partner.company_id)

        if bad_partners:
            raise UserError(
                _(
                    "Split-company invoicing requires shared contacts. "
                    "These contacts are company-specific: %s"
                )
                % ", ".join(bad_partners.mapped("display_name"))
            )

    def _get_split_fiscal_position(self, company):
        self.ensure_one()

        if self.fiscal_position_id:
            fiscal_position = self.env["account.fiscal.position"].sudo().search(
                [
                    ("company_id", "=", company.id),
                    ("name", "=", self.fiscal_position_id.name),
                ],
                limit=1,
            )
            if fiscal_position:
                return fiscal_position

        return self.env["account.fiscal.position"].with_company(company)._get_fiscal_position(
            self.partner_invoice_id
        )

    def _get_split_partner_bank(self, company):
        self.ensure_one()

        return self.env["res.partner.bank"].sudo().search(
            [
                ("partner_id", "=", company.partner_id.id),
                "|",
                ("company_id", "=", company.id),
                ("company_id", "=", False),
            ],
            limit=1,
        )

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()

        company = self.current_invoice_company_id
        if not company:
            return invoice_vals

        fiscal_position = self._get_split_fiscal_position(company)
        partner_bank = self._get_split_partner_bank(company)

        invoice_vals.update(
            {
                "company_id": company.id,
                "partner_bank_id": partner_bank.id or False,
                "fiscal_position_id": fiscal_position.id if fiscal_position else False,
            }
        )

        return invoice_vals

    def _create_invoices(self, grouped=False, final=False, date=None):
        all_moves = self.env["account.move"]

        for original_order in self:
            original_order._validate_split_invoice_partners()

            companies = original_order._get_split_invoice_companies(final=final)
            if not companies:
                continue

            try:
                for company in companies:
                    fiscal_position = original_order._get_split_fiscal_position(company)

                    allowed_company_ids = set(
                        self.env.context.get(
                            "allowed_company_ids",
                            self.env.user.company_ids.ids,
                        )
                    )
                    allowed_company_ids.add(company.id)
                    allowed_company_ids.add(original_order.company_id.id)

                    original_order.current_invoice_company_id = company.id

                    order = original_order.with_company(company).with_context(
                        default_company_id=company.id,
                        allowed_company_ids=list(allowed_company_ids),
                        split_fiscal_position_id=fiscal_position.id
                        if fiscal_position
                        else False,
                    )

                    moves = super(SaleOrder, order)._create_invoices(
                        grouped=grouped,
                        final=final,
                        date=date,
                    )

                    wrong_moves = moves.filtered(lambda move: move.company_id != company)
                    if wrong_moves:
                        raise UserError(
                            _("Invoice company mismatch while invoicing sale order %s.")
                            % original_order.name
                        )

                    all_moves |= moves

            finally:
                original_order.current_invoice_company_id = False

        return all_moves

    def _get_reward_line_values(self, reward, coupon, **kwargs):
        res = super()._get_reward_line_values(reward, coupon, **kwargs)

        for line_vals in res:
            line_vals["company_id"] = self.company_id.id

        return res