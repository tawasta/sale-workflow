from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_id = fields.Many2one(
        check_company=False,
    )

    @api.model
    def create(self, values):
        res = super().create(values)

        for record in self:
            if (
                record.product_id
                and record.product_id.company_id
                and record.product_id.company_id != record.company_id
            ):
                record.company_id = record.product_id.company_id.id

        return res

    def write(self, values):
        res = super().write(values)

        for record in self:
            if (
                record.product_id
                and record.product_id.company_id
                and record.product_id.company_id != record.company_id
            ):
                record.company_id = record.product_id.company_id.id

        return res

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)

        if self.order_id.current_invoice_company_id:
            # Override some company-specific line values
            company = self.order_id.current_invoice_company_id

            if res.get("account_id"):
                # Fetch a matching account
                # TODO: add an option to use the default account from product (for this company)
                account = (
                    self.env["account.account"]
                    .sudo()
                    .search(
                        [
                            ("company_id", "=", company.id),
                            ("code", "=", res["account_id"]),
                        ]
                    )
                )

                if account:
                    res["account_id"] = account.id

            if res.get("tax_ids"):
                # Change taxes
                tax_names = self.tax_id.mapped("name")

                taxes = (
                    self.env["account.tax"]
                    .sudo()
                    .search(
                        [
                            ("company_id", "=", company.id),
                            ("name", "in", tax_names),
                            ("type_tax_use", "=", "sale"),
                        ]
                    )
                )
                if taxes:
                    res["tax_ids"] = [(6, 0, taxes.ids)]
        return res
