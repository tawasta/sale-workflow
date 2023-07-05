from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    partner_id = fields.Many2one(
        domain="[('type', 'in', ['contact', 'private']), "
        "'|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )
