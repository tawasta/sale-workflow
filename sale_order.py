# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _

class sale_order(osv.Model):

    _inherit = 'sale.order'

    _columns = {
        'customer_contact': fields.many2one('res.partner', "Customer's contact"),
    }
