from openerp.osv import osv, fields
from openerp.tools.translate import _

class Partner(osv.Model):
    
    _inherit = 'res.partner'

    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if 'show_only_top_level' in context:
            matches = []
            if not args:
                args = []
            if context is None:
                context = {}            
            if name:
                #matches = self.search(cr, user, ['|','|', ('lvl1_name','ilike',name),('lvl2_name','ilike',name), ('lvl3_name', 'ilike', name)] + args, limit=limit, context=context)
                matches = self.search(cr, user, ['&', '&', ('is_company','=',True), ('parent_id','=',False), '|', ('lvl1_name','ilike',name), '|', ('lvl2_name','ilike',name), ('lvl3_name', 'ilike', name)] + args, limit=limit, context=context)
    
            # If empty search parameter, return full list
            else:
                matches = self.search(cr, user, ['&', ('is_company','=',True), ('parent_id','=',False)] + args, limit=limit, context=context)
                
            return self.name_get(cr, user, matches, context)
        else:
            return super(Partner, self).name_search(cr, user, name, context=context)
            
    ''' 
    # When the selected country or is_company is changed, check if the business id should be set to be mandatory:
    # Mandatory if country = finland and is_company = true
    def business_id_and_vat_change(self, cr, uid, ids, country_id, is_company, parent_id, context=None):
        #res = super(Partner, self).onchange_method(cr, uid, ids, context=context)
        
        
        if country_id is False:
            val = { 'businessid_required': False, 'vatnumber_required': False }
            return {'value': val } 
        else:
            # List of all countries that trigger the business id condition
            b_id_check_countries = ['Finland']
    
            country_obj = self.pool.get('res.country')
            selected_country = country_obj.browse(cr, uid, [country_id])[0]
            
            name = selected_country['name']
            
            val={}
            
            if name in b_id_check_countries and is_company is True and parent_id is False:
                #val = { 'businessid_required': True }
                val['businessid_required'] = True
            else:
                #val = { 'businessid_required': False }
                val['businessid_required'] = False
                
                
            # List of all countries that trigger the vat condition.
            vat_check_countries = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark',
                               'Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania',
                               'Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia',
                               'Spain','Sweden','United Kingdom']                
                
            if name in vat_check_countries and is_company is True and parent_id is False:
                val['vatnumber_required'] = True
            else:
                val['vatnumber_required'] = False               
                
            
            return {'value': val } 
    '''
                

    def business_id_and_vat_change(self, cr, uid, ids, country_id, is_company, parent_id, context=None):
        #res = super(Partner, self).onchange_method(cr, uid, ids, context=context)
        
        
        if country_id is False:
            val = { 'businessid_shown': False, 'vatnumber_shown': False }
            return {'value': val } 
        else:
            # List of all countries that trigger the business id condition
            b_id_check_countries = ['Finland']
    
            country_obj = self.pool.get('res.country')
            selected_country = country_obj.browse(cr, uid, [country_id])[0]
            
            name = selected_country['name']
            
            val={}
            
            if name in b_id_check_countries and is_company is True and parent_id is False:
                #val = { 'businessid_required': True }
                val['businessid_shown'] = True
            else:
                #val = { 'businessid_required': False }
                val['businessid_shown'] = False
                
                
            # List of all countries that trigger the vat condition.
            vat_check_countries = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark',
                               'Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania',
                               'Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia',
                               'Spain','Sweden','United Kingdom']                
                
            if name in vat_check_countries and is_company is True and parent_id is False:
                val['vatnumber_shown'] = True
            else:
                val['vatnumber_shown'] = False               
                
            
            return {'value': val } 
        
    _columns = {
        'businessid': fields.char(string="Business id", size=20),
        
        # Helper fields that are never shown to users but are used with the onchange methods to set businessid/vat fields to required=true or false
        #'businessid_required': fields.boolean(string='Business ID required'),
        #'vatnumber_required': fields.boolean(string='Vat required'),
        'businessid_shown': fields.boolean(string='Business ID shown'),
        'vatnumber_shown': fields.boolean(string='Vat shown'),
    }
    
    _defaults = {
        #'businessid_required': False,
        #'vatnumber_required': False,   
        'businessid_shown': False,
        'vatnumber_shown': False,                
    }    

    _sql_constraints = [
        ('businessid_unique', 'unique(businessid)', _('The business ID already exists for another customer.'))
    ]
