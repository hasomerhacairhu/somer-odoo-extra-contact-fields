{
    'name': 'Exit Date in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds an ExitDate field to Odoo Contacts',
    'description': """
This module adds a custom ExitDate field to Contacts (res.partner), allowing
users to store the date on which a contact (user) left.
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
