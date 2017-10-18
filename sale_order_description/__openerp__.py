# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015- Oy Tawasta Technologies Ltd. (http://www.tawasta.fi)
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
    'name': 'Sale Order Description',
    'category': 'Sale',
    'version': '8.0.1.0.1',
    'author': 'Oy Tawasta Technologies Ltd.',
    'website': 'http://www.tawasta.fi',
    'installable': False,    
    'depends': [
        'sale',
    ],
    'description': '''
Sale Order Description
======================

Adds a description (an internal note) to sale order


Features
========
* Adds description field
* Adds description notebook page
''',
    'data': [
        'views/sale_order.xml',
    ],
}
