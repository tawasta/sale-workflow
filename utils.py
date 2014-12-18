# -*- coding: utf-8 -*-
def check_vat_country(country_name):
        vat_check_countries = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark',
                           'Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania',
                           'Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia',
                           'Spain','Sweden','United Kingdom']
        
        if country_name in vat_check_countries:
            return True
        else:
            return False

def check_businessid_country(country_name):
        businessid_check_countries = ['Finland']
        
        if country_name in businessid_check_countries:
            return True
        else:
            return False