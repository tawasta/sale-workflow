from openerp.osv import osv, fields
from tools.translate import _

class Partner(osv.Model):
    
    _inherit = 'res.partner'
    
    
    # When the selected country or is_company is changed, check if the business id should be set to be mandatory:
    # Mandatory if country = finland and is_company = true
    def business_id_change(self, cr, uid, ids, country_id, is_company, parent_id, context=None):

        if country_id is False or parent_id is not False:
            return {}
        
        # List of all countries that trigger the condition. Use only Finland.
        b_id_check_countries = ['Finland']

        country_obj = self.pool.get('res.country')
        selected_country = country_obj.browse(cr, uid, [country_id])[0]
        
        name = selected_country['name']
        
        if name in b_id_check_countries and is_company is True:
            val = { 'businessid_required': True }
        else:
            val = { 'businessid_required': False }
        
        return {'value': val } 
        
    _columns = {
        'businessid': fields.char(string="Business id", size=20),
        
        # A helper field that is never shown to users but is used with the onchange methods to set businessid field to required=true or false
        'businessid_required': fields.boolean(string='Business ID required'),
    }
    
    _defaults = {
        'businessid_required': False,
    }    

    _sql_constraints = [
        ('businessid_unique', 'unique(businessid)', _('The business ID already exists for another customer.'))
    ]
