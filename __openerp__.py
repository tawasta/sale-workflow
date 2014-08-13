# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2013- Vizucom Oy (http://www.vizucom.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Business ID and VAT fields',
    'category': 'Sale',
    'version': '0.1',
    'author': 'Vizucom Oy',
    'depends': ['base_vat','base_misc_modules_menuitem'],
    'description': """
Business ID and VAT fields handling
===================================
* Adds a new business ID field 
* Shows business ID and existing TIN fields only for appropriate companies, based on their country (bID for Finland, TIN for EU-based countries)
* Adds a settings window for defining whether to show bID/TIN just for top-level companies, or affiliates also
* Restricts business IDs so that they must be unique
* Uses the standard VIES VAT check functionality in OE core for checking the TIN authenticity

""",
    'data': [
            'view/partner.xml',
            'view/sbid_settings.xml',
            'data/sbid_data.xml',
            'security/ir.model.access.csv',
    ],
}
