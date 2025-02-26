{
    'name': 'Exit Reason in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds an ExitReason field that is visible only if Exit Date is provided',
    'description': """
This module adds a field 'exit_reason' to contacts.
If the 'exit_date' field (from exit_date_contact) is not set, then the exit_reason field is hidden.
""",
    'author': 'Adrian',
    'license': 'LGPL-3',
    'depends': ['contacts', 'exit_date_contact'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
