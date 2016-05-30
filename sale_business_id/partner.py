from openerp.osv import osv, fields
from openerp.tools.translate import _
from utils import check_vat_country, check_businessid_country

class Partner(osv.Model):
    
    _inherit = 'res.partner'

    def _init_business_id_and_vat(self, cr, uid, ids=None, context=None):
        return False
        ''' If customer data was imported to Odoo before the module installation,
        the business id and vat fields won't get shown until the onchange function
        gets triggered. To avoid this, loop through partner data when the module
        is installed and assign the two "_shown" boolean fields. '''
        
        all_partner_ids         = self.search(cr, uid, args=[])
        vat_write_ids           = []
        businessid_write_ids    = []
        
        settings_model = self.pool.get('sale_business_id.settings')
        show_for_affiliates = settings_model.read(cr, uid, 1, ['show_bid_vat_for_affiliates'], context)['show_bid_vat_for_affiliates']
                
        ''' Browse without context to avoid getting translated names '''
        
        if show_for_affiliates:
            for partner in self.browse(cr, uid, all_partner_ids):
                if partner.is_company and check_vat_country(partner.country_id.name):
                    vat_write_ids.append(partner.id)
                if partner.is_company and check_businessid_country(partner.country_id.name):
                    businessid_write_ids.append(partner.id)            
        else:
            for partner in self.browse(cr, uid, all_partner_ids):
                if partner.is_company and not partner.parent_id and check_vat_country(partner.country_id.name):
                    vat_write_ids.append(partner.id)
                if partner.is_company and not partner.parent_id and check_businessid_country(partner.country_id.name):
                    businessid_write_ids.append(partner.id)
        
        
        self.write(cr, uid, vat_write_ids, { 'vatnumber_shown': True})
        print "Set %i partners' VAT fields visible " % len(vat_write_ids)
        
        self.write(cr, uid, businessid_write_ids, { 'businessid_shown': True})
        print "Set %i partners' Business ID fields visible " % len(businessid_write_ids)     
        
    


    def business_id_and_vat_change(self, cr, uid, ids, country_id, is_company, parent_id, context=None):
        ''' Gets triggered in other fields' onchange and defines whether 
        the business ID and VAT fields are visible to the user '''
                        
        if not country_id:
            val = { 
                'businessid_shown': False, 
                'vatnumber_shown': False 
            }
            return {'value': val } 
        else:
    
            ''' Pull from settings info about whether to show bID/VAT for affiliates as well as toplevel partners '''
            settings_model = self.pool.get('sale_business_id.settings')
            show_for_affiliates = settings_model.read(cr, uid, 1, ['show_bid_vat_for_affiliates'], context)['show_bid_vat_for_affiliates']
                
            country_obj = self.pool.get('res.country')
            selected_country = country_obj.browse(cr, uid, [country_id])[0]
            name = selected_country['name']
            
            val={}
            
            if show_for_affiliates:
                if check_businessid_country(name) and is_company:
                    val['businessid_shown'] = True
                else:
                    val['businessid_shown'] = False
                    
                if check_vat_country(name) and is_company:
                    val['vatnumber_shown'] = True
                else:
                    val['vatnumber_shown'] = False                       
                    
            else:
                if check_businessid_country(name) and is_company and not parent_id:
                    val['businessid_shown'] = True
                else:
                    val['businessid_shown'] = False           

                if check_vat_country(name) and is_company and not parent_id:
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

    _sql_constraints = [
        ('businessid_unique', 'unique(businessid)', _('The business ID already exists for another partner.'))
    ]
