{
    'name': 'Next Birthday in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Shows the next birthday date based on the Birthday field',
    'description': """
Adds a read-only Next Birthday field to res.partner (Contacts) that is computed from 
the existing Birthday field. If no birthday is set, this field is empty and not editable.
""",
    'author': 'Adrian',
    'license': 'LGPL-3',
    'depends': ['birthdate_contact',
        'contacts', 
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
