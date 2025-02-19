{
    'name': 'entry_date_contact',
    'version': '18.0.1.0.0',
    'category': 'Custom',
    'summary': 'Adds an EntryDate field to Contacts and updates it when user logs in',
    'description': """ This module adds a 'entry_date' Date field on Contacts (res.partner), 
     which updates dynamically to the user's last login date.""",
    'author': 'Adrian',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

