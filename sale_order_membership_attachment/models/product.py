from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    membership_attachment_ids = fields.Many2many("ir.attachment", string="Attachments")
