{
    'name': 'Membership Level in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Add a MembershipLevel dropdown field to Contacts, loaded from a JSON file',
    'description': """
This module adds a dropdown field called 'MembershipLevel' to res.partner (Contacts). 
The available options (A, B, C) are stored in a configurable membership_levels.json file.
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
