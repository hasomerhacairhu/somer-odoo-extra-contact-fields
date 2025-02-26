{
    'name': 'Nickname in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a Nickname field to Odoo Contacts',
    'description': """
Adds a Char field 'Nickname' to res.partner (Contacts),
allowing you to store a contact's nickname.
""",
    'author': 'Your Name',
    'license': 'LGPL-3',
    'depends': ['contacts'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
