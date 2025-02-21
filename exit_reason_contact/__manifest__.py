{
    'name': 'Exit Reason in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds an ExitReason field that is only visible if ExitDate is set',
    'description': """
This module adds a field 'ExitReason' to res.partner (Contacts). 
It will only appear on the form view if 'ExitDate' has a value, and it will 
disappear again if 'ExitDate' is removed. 
""",
    'author': 'Adrian',
    'license': 'LGPL-3',
    'depends': ['exit_date_contact',
        'contacts' 
    ],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
