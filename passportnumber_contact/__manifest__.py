{
    'name': 'PassportNumber in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a PassportNumber field to Odoo Contacts',
    'description': """
Adds a Char field 'passport_number' to res.partner (Contacts),
allowing you to store the contact's Passport Number as a string.
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
