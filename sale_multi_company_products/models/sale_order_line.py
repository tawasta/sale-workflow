from odoo import _, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)

        company = self.order_id.current_invoice_company_id
        if not company or self.display_type:
            return res

        product = self.product_id.with_company(company)

        fiscal_position = self.env["account.fiscal.position"].browse(
            self.env.context.get("split_fiscal_position_id")
        )

        account = (
            product.property_account_income_id
            or product.categ_id.with_company(company).property_account_income_categ_id
        )

        if fiscal_position and account:
            account = fiscal_position.map_account(account)

        if not account:
            raise UserError(
                _(
                    "No income account found for product '%(product)s' "
                    "in company '%(company)s'."
                )
                % {
                    "product": product.display_name,
                    "company": company.display_name,
                }
            )

        taxes = product.taxes_id.filtered(lambda tax: tax.company_id == company)
        if fiscal_position:
            taxes = fiscal_position.map_tax(taxes)

        res.update(
            {
                "company_id": company.id,
                "account_id": account.id,
                "tax_ids": [(6, 0, taxes.ids)],
            }
        )

        return res
