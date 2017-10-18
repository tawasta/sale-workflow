# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2016 Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################
{
    'name': 'Customer Contact with several companies for sale orders',
    'summary': 'Customer Contact for sale orders that works with partner contact in several companies',
    'version': '8.0.0.2.0',
    'category': 'Sales',
    'website': 'http://www.tawasta.fi',
    'author': 'Oy Tawasta Technologies Ltd., Vizucom Oy',
    'license': 'AGPL-3',
    'application': False,
    'installable': False,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'sale_order_customer_contact',
        'partner_contact_in_several_companies',
    ],
    'data': [
        'views/sale_order.xml',
    ],
    'demo': [
    ],
}
