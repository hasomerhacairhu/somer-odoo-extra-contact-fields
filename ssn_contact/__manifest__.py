{
    'name': 'SSN in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds an SSN (string) field to Odoo Contacts',
    'description': """
Adds a Char field 'SSN' to res.partner (Contacts),
allowing you to store the contact's social security number as a string.
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
