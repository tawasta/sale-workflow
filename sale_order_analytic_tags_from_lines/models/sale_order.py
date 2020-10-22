from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    order_line_analytic_tags = fields.Many2many(
        comodel_name='account.analytic.tag',
        string='Analytic tags from lines',
        compute='compute_order_line_analytic_tags')

    def compute_order_line_analytic_tags(self):
        for sale in self:
            for line in sale.order_line:
                sale.order_line_analytic_tags += line.analytic_tag_ids
