{
    'name': 'Stakeholder Group in Contacts',
    'version': '18.0.1.0',
    'category': 'Contacts',
    'summary': 'Adds a multi-select StakeholderGroup field to Contacts from a JSON file',
    'description': """
This module creates a separate model `stakeholder.group` with possible stakeholder groups
loaded from a JSON file. The `res.partner` model gets a Many2many field to that model,
enabling a multi-select dropdown of stakeholder groups.
""",
    'author': 'Adrian',
    'license': 'LGPL-3',
    'depends': ['contacts'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
    'application': True,
    'post_init_hook': 'post_init_hook',
}
