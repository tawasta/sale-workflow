# -*- coding: utf-8 -*-
from odoo import api, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.onchange('project_id')
    def onchange_project_id_update_analytic_tags(self):
        for record in self:
            if record.project_id and \
                    record.project_id.tag_ids:

                for line in record.order_line:
                    line.analytic_tag_ids += record.project_id.tag_ids
