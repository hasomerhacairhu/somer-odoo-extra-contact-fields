{
    'name': 'Is Vaccinated in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a field to store whether the contact is vaccinated',
    'description': """
This module adds a boolean field to res.partner (Contacts) indicating if the contact is vaccinated.
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
