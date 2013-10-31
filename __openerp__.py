#
# Kopar Project Fields
# Vizucom 2013
#
{
    'name': 'Business ID',
    'category': 'CRM',
    'version': '0.1',
    'author': 'Vizucom Oy',
    'depends': ['sale_customer_names'],
    'description': """
Adds a mandatory, unique business ID field for all customers that are companies.
""",
    'data': [
            'view/partner.xml',
            'view/sale_order.xml',
    ],
}
