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
        # Tämä on pakollinen tässä arkkitehtuurissa:
        # sale.order kuuluu verkkokauppayhtiölle, mutta tuotteet voivat kuulua eri variant_company_id-yhtiöille.
        return

    def _get_invoiceable_lines(self, final=False):
        lines = super()._get_invoiceable_lines(final=final)

        if self.current_invoice_company_id:
            lines = lines.filtered(
                lambda line: (
                    line.display_type
                    or line.product_id.variant_company_id == self.current_invoice_company_id
                )
            )

        return lines

    def _get_split_base_invoiceable_lines(self, final=False):
        self.ensure_one()
        return super(SaleOrder, self)._get_invoiceable_lines(final=final).filtered(
            lambda line: not line.display_type
        )

    def _get_split_invoice_companies(self, final=False):
        self.ensure_one()

        lines = self._get_split_base_invoiceable_lines(final=final)

        missing_company_lines = lines.filtered(
            lambda line: not line.product_id.variant_company_id
        )
        if missing_company_lines:
            raise UserError(
                _("Variant company is missing from products on these order lines: %s")
                % ", ".join(missing_company_lines.mapped("name"))
            )

        return lines.mapped("product_id.variant_company_id")

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

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()

        company = self.current_invoice_company_id
        if not company:
            return invoice_vals

        fiscal_position = self._get_split_fiscal_position(company)

        invoice_vals.update({
            "company_id": company.id,
            "partner_bank_id": company.partner_id.bank_ids[:1].id,
            "fiscal_position_id": fiscal_position.id if fiscal_position else False,
        })

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
                        split_fiscal_position_id=fiscal_position.id if fiscal_position else False,
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