# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def _compute_surcharge(self):
        # Informative fields for showing what surcharge product and percentage
        # are set for the current company
        for partner in self:
            partner.surcharge_product_id \
                = self.env.user.company_id.surcharge_product_id.id
            partner.surcharge_percentage \
                = self.env.user.company_id.surcharge_percentage

    surcharge_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Surcharge Product',
        compute=_compute_surcharge,
        readonly=True,
    )

    surcharge_percentage = fields.Float(
        string='Surcharge %',
        digits=(6, 2),
        compute=_compute_surcharge,
        readonly=True,
    )

    apply_surcharge = fields.Boolean(
        string='Apply surcharge',
        help=('''If checked, a surcharge % defined above is automatically added
              to this customer's sale orders as a new order line''')
    )
