{
    'name': 'TaxID in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a TaxID field to Odoo Contacts',
    'description': """
This module adds a Char field 'TaxID' to res.partner (Contacts),
allowing you to store the contact's Tax Identification Number as a string.
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
