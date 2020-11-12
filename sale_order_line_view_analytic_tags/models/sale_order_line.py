
from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    # Set store to True so that the grouping works. Else Odoo gives an error
    analytic_tag_name = fields.Char(
        compute="_compute_analytic_tag_names",
        search="_search_analytic_tag_names",
        store=True,
    )

    @api.multi
    def _search_analytic_tag_names(self, operator, value):
        recs = self.search([]).filtered(
            lambda x: x.analytic_tag_name)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    @api.multi
    @api.depends('analytic_tag_ids')
    def _compute_analytic_tag_names(self):
        lines = self.env['sale.order.line'].search(
                [('analytic_tag_ids','!=',False)])
        for line in lines:
            names = [x.name for x in line.analytic_tag_ids]
            names.sort()
            line.analytic_tag_name = ', '.join(names)
