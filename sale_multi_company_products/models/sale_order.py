from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    current_invoice_company_id = fields.Many2one(
        string="Current company to invoice",
        help="This field is for technical use only",
        comodel_name="res.company",
        readonly=True,
        copy=False,
    )

    def _check_order_line_company_id(self):
        # Override cross-company product check
        return

    def _create_invoices(self, grouped=False, final=False, date=None):
        for order in self:
            lines = order._get_invoiceable_lines()

            companies = lines.mapped("product_id.company_id")
            if len(companies) == 1 and companies == self.company_id:
                # No custom processing for one company
                return super()._create_invoices(grouped, final, date)

            moves = self.env["account.move"]
            for company in companies:
                # Set a temporary company values
                order = order.with_company(company.id).with_context(
                    default_company_id=company.id
                )
                order.current_invoice_company_id = company.id
                moves += super()._create_invoices(grouped, final, date)

            # Set the correct company and unset the temporary company
            order.current_invoice_company_id = False

        # Only return user company moves to prevent access error
        moves = moves.filtered(lambda r: r.company_id == self.env.user.company_id)

        return moves

    def _get_invoiceable_lines(self, final=False):
        lines = super()._get_invoiceable_lines(final)

        if self.current_invoice_company_id:
            lines = lines.filtered(
                lambda r: r.product_id.company_id == self.current_invoice_company_id
            )

        return lines

    def _prepare_invoice(self):
        if self.current_invoice_company_id:
            company = self.current_invoice_company_id
            self = self.with_company(company.id).with_context(
                default_company_id=company.id
            )

        invoice_vals = super()._prepare_invoice()
        if self.current_invoice_company_id:
            invoice_vals["company_id"] = self.current_invoice_company_id.id
            invoice_vals["partner_bank_id"] = company.partner_id.bank_ids[:1].id
            fiscal_position_model = self.env["account.fiscal.position"]
            old_fiscal_position = fiscal_position_model.browse(
                [invoice_vals["fiscal_position_id"]]
            )

            fiscal_position = fiscal_position_model.sudo().search(
                [
                    ("company_id", "=", company.id),
                    ("name", "=", old_fiscal_position.name),
                ]
            )
            if fiscal_position:
                invoice_vals["fiscal_position_id"] = fiscal_position.id

        return invoice_vals
