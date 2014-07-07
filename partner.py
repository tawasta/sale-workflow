from openerp.osv import osv, fields
from openerp.tools.translate import _

class Partner(osv.Model):
    
    _inherit = 'res.partner'

    ''' Gets triggered in other fields' onchange and defines whether 
    the business ID and VAT fields are visible to the user '''
    def business_id_and_vat_change(self, cr, uid, ids, country_id, is_company, parent_id, context=None):
        
        if country_id is False:
            val = { 'businessid_shown': False, 'vatnumber_shown': False }
            return {'value': val } 
        else:
            ''' List of all countries that trigger the business id condition '''
            b_id_check_countries = ['Finland']
    
            country_obj = self.pool.get('res.country')
            selected_country = country_obj.browse(cr, uid, [country_id])[0]
            
            name = selected_country['name']
            
            val={}
            
            if name in b_id_check_countries and is_company is True and parent_id is False:
                val['businessid_shown'] = True
            else:
                #val = { 'businessid_required': False }
                val['businessid_shown'] = False
                
                
            ''' List of all countries that trigger the vat condition. '''
            vat_check_countries = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark',
                               'Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania',
                               'Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia',
                               'Spain','Sweden','United Kingdom']                
                
            if name in vat_check_countries and is_company is True and parent_id is False:
                val['vatnumber_shown'] = True
            else:
                val['vatnumber_shown'] = False               
                
            
            return { 'value': val } 

    ''' "_shown" fields are helpers that are never shown to users but are used with 
    onchange methods to set businessid/vat fields to invisible=true or false '''
        
    _columns = {
        'businessid': fields.char(string="Business id", size=20),
        'businessid_shown': fields.boolean(string='Business ID shown'),
        'vatnumber_shown': fields.boolean(string='Vat shown'),
    }
    
    _defaults = {
        'businessid_shown': False,
        'vatnumber_shown': False,                
    }    

    _sql_constraints = [
        ('businessid_unique', 'unique(businessid)', _('The business ID already exists for another partner.'))
    ]
