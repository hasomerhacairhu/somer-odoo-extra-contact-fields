{
    'name': 'Madrich Training in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a field to indicate Madrich training for contacts',
    'description': """
This module adds a Boolean field to res.partner (Contacts) indicating if the contact had Madrich training.
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
