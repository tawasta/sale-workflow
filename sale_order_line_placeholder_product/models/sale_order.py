from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        self.check_code()

        return super(SaleOrder, self).action_confirm()

    @api.multi
    def check_code(self):
        for order in self:
            for line in order.order_line:
                if line.product_id.additional_code:
                    raise ValidationError(
                        _("Please replace the placeholder product %s")
                        % line.product_id.name
                    )


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    old_product_id = fields.Text(string="Old Product Id", default="")

    @api.multi
    @api.onchange("product_id")
    def product_id_change(self):

        if self._origin.product_id.additional_code:
            self.old_product_id = self._origin.name
        else:
            self.old_product_id = ""

        res = super(SaleOrderLine, self).product_id_change()

        if self.old_product_id:
            nextline = "\n"
        else:
            nextline = ""

        if self.product_id.description_sale:
            self.name = "{}\n{}{}{}".format(
                self.product_id.name,
                self.product_id.description_sale,
                nextline,
                self.old_product_id,
            )
        elif self.product_id:
            self.name = "{}{}{}".format(
                self.product_id.name, nextline, self.old_product_id
            )

        return res
