{
    'name': 'Passport Expiration Date in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a field for storing the passport\'s expiration date',
    'description': """
This module adds a field to res.partner (Contacts) to store a passport expiration date.
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
