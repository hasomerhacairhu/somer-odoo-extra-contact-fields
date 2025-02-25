{
    'name': 'Place of Birth in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a field to store place of birth for contacts',
    'description': """
This module adds a field to res.partner (Contacts) to store a contact's place of birth.
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
