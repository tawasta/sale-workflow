# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    analytic_tag_ids = fields.Many2many(
        default=lambda self: self._default_get_analytic_tag_ids()
    )

    def _default_get_analytic_tag_ids(self):
        res = False

        project_id = self._context.get('project_id')
        if project_id:
            project = self.env['account.analytic.account'].browse([project_id])

            res = project.tag_ids

        return res
