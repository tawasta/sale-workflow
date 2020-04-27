from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    sales_contact = fields.Many2one(string="Sales contact", comodel_name="res.partner")
