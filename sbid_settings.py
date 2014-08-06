# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _


class sbid_settings(osv.osv):
    _name = "sale_business_id.settings"

    _columns = {
        'show_bid_vat_for_affiliates': fields.boolean('Show business ID and VAT fields for affiliates'),  
    }
    
    
