from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    membership_attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        relation="product_template_membership_attachment_rel",
        column1="product_template_id",
        column2="attachment_id",
        string="Membership Product Attachments",
    )
