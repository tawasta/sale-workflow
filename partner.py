from openerp.osv import osv, fields
from tools.translate import _

class Partner(osv.Model):
    
    _inherit = 'res.partner'
    
    '''
    def name_get(self, cr, uid, ids, context=None):
        if 'show_only_top_level' in context:
            if isinstance(ids, (list, tuple)) and not len(ids):
                reads = self.read(cr, uid, ids, ['name', 'is_company','parent_id', 'type'], context=context)
                res = []
                for record in reads:
                    res.append((record['id'], name))
                return res
            if isinstance(ids, (long, int)):
                ids = [ids]
    
            #reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
            reads = self.read(cr, uid, ids, ['name','lvl1_name', 'lvl2_name','lvl3_name','is_company','parent_id'], context=context)
            res = []
            for record in reads:
                #name = record['name']
                
                is_company = record['is_company']
                parent_id = record['parent_id']
                
                if is_company is False or parent_id is not False:
                    res.append((record['id'], record['name']))
                    continue
                
                
                # Fallback to those records that were created prior to installing this module and dont have the new fields
                if record['lvl1_name'] == "" or record['lvl1_name'] == False:
                    res.append((record['id'], record['name']))
                # New name generation
                else:
                    new_name = record['lvl1_name']
                    if record['lvl2_name'] != "" and record['lvl2_name'] != False:
                        new_name += ", " +  record['lvl2_name']
                    if record['lvl3_name'] != "" and record['lvl3_name'] != False:
                        new_name += ", " +  record['lvl3_name']
                    res.append((record['id'], new_name))
    
            return res
        else:
            return super(Partner, self).name_get(cr, uid, ids, context=context)
    '''
        
        
        
    '''
        #reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        reads = self.read(cr, uid, ids, ['name','lvl1_name', 'lvl2_name','lvl3_name'], context=context)
        res = []
        for record in reads:
            #name = record['name']
            #is_company = record['is_company']
            #parent_id = record['parent_id']
            
            
            # Fallback to those records that were created prior to installing this module and dont have the new fields
            if record['lvl1_name'] == "" or record['lvl1_name'] == False:
                res.append((record['id'], record['name']))
            # New name generation
            else:
                new_name = record['lvl1_name']
                if record['lvl2_name'] != "" and record['lvl2_name'] != False:
                    new_name += ", " +  record['lvl2_name']
                if record['lvl3_name'] != "" and record['lvl3_name'] != False:
                    new_name += ", " +  record['lvl3_name']
                res.append((record['id'], new_name))

        return res
    '''
    
    '''
    is_company = True AND parent_id = False AND (lvl1_name ilike name OR lvl2_name ilike name OR lvl3_name ilike name)
    
    (is_company = True AND parent_id = False) AND (lvl1_name ilike name OR lvl2_name ilike name OR lvl3_name ilike name)
    
    AND (is_company = True AND parent_id = False) (lvl1_name ilike name OR lvl2_name ilike name OR lvl3_name ilike name)
    
    AND (AND is_company = True parent_id = False) (lvl1_name ilike name OR lvl2_name ilike name OR lvl3_name ilike name)
    
    AND (AND is_company = True parent_id = False) (lvl1_name ilike name OR (lvl2_name ilike name OR lvl3_name ilike name))

    AND (AND is_company = True parent_id = False) (OR lvl1_name ilike name (lvl2_name ilike name OR lvl3_name ilike name))
    
    AND (AND is_company = True parent_id = False) (OR lvl1_name ilike name (OR  lvl2_name ilike name  lvl3_name ilike name))
    
    -->
     ) (OR lvl1_name ilike name (OR  lvl2_name ilike name  lvl3_name ilike name)) 
    ['&', '&', ('is_company','=',True), ('parent_id','=',False), '|', ('lvl1_name','ilike',name), '|', ('lvl2_name','ilike',name), ('lvl3_name', 'ilike', name)]  
    
    
    
    ['&', '&', ('is_company','=',True), ('parent_id','=',False), '|', ('lvl1_name','ilike',name), '|', ('lvl2_name','ilike',name), ('lvl3_name', 'ilike', name)]    
    
    
    '''
    
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
                
                  
                
                #ids = self.search(cr, user, [('kanban_lvl1_name','=',"Ostolaskut")], limit=limit, context=context)
    
            # If empty search parameter, return full list
            else:
                matches = self.search(cr, user, ['&', ('is_company','=',True), ('parent_id','=',False)] + args, limit=limit, context=context)
                
                
            return self.name_get(cr, user, matches, context)
        else:
            return super(Partner, self).name_search(cr, user, name, context=context)
            
        
    # When the selected country or is_company is changed, check if the business id should be set to be mandatory:
    # Mandatory if country = finland and is_company = true
    def business_id_change(self, cr, uid, ids, country_id, is_company, parent_id, context=None):
        #res = super(Partner, self).onchange_method(cr, uid, ids, context=context)
        
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
