{
    'name': 'Birthday in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Add a BirthDate field to Odoo Contacts',
    'description': """
Adds a date-type field called 'BirthDate' (birthday) to Contacts (res.partner),
and displays it in the contact form.
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
