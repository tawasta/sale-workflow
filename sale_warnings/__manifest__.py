##############################################################################
#
#    Copyright 2026 Tawasta OS Technologies
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Sale Warnings",
    "category": "Sales",
    "version": "19.0.1.0.0",
    "installable": True,
    "author": "Futural",
    "license": "AGPL-3",
    "website": "https://github.com/tawasta/sale-workflow",
    "depends": ["sale"],
    "data": [
        "views/sale_order.xml",
        "views/res_partner.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sale_warnings/static/src/js/sale_order.esm.js",
            "sale_warnings/static/src/xml/sale_order.xml",
        ]
    },
}
