{
    'name': 'ID Number in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds an IDNumber (string) field to Odoo Contacts',
    'description': """
Adds a Char field 'IDNumber' to res.partner (Contacts),
allowing you to store a contact's ID number as a string.
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
