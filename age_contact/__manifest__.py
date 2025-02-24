{
    'name': 'Age in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds an Age field to Contacts, computed from the BirthDate field',
    'description': """
Automatically computes a contact's age (integer) from the BirthDate field,
which is provided by the 'birthdate_contact' module.
""",
    'author': 'Adrian',
    'license': 'LGPL-3',
    'depends': [
        'contacts',
        'birthdate_contact',
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
