#
# Kopar Project Fields
# Vizucom 2013
#
{
    'name': 'Business ID and VAT fields',
    'category': 'Sale',
    'version': '0.1',
    'author': 'Vizucom Oy',
    'depends': ['sale_customer_names','account','base_vat'],
    'description': """
Adds a business ID field for Finnish companies, and hides the VAT field from non-european companies
""",
    'data': [
            'view/partner.xml',
            'view/sale_order.xml',
            'view/account_invoice.xml',
    ],
}
