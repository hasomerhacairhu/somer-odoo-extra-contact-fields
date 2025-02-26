{
    'name': 'T-Shirt Size in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a TShirtSize dropdown field to Contacts, reading size options from JSON',
    'description': """
This module reads possible T-shirt sizes (XS, S, M, L, XL, XXL, 3XL, 4XL, 5XL) 
from a JSON file (tshirt_sizes.json) and stores a single selection field (tshirt_size) 
on Contacts (res.partner).
""",
    'author': 'Adrian',
    'license': 'LGPL-3',
    'depends': ['contacts'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
