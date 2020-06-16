# from openerp.osv import osv,fields
# from openerp import api
# from datetime import date,datetime, timedelta
# import time
# import openerp.addons.decimal_precision as dp
# from openerp.tools.translate import _
from odoo import fields, models


class sale_order_inherit(models.Model):
    _inherit = 'sale.order'

    sale_type = fields.Many2one(
        comodel_name="sale.type"
    )
