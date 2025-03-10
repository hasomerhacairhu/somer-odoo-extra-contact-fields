{
    'name': 'Family Connections in Contacts',
    'version': '1.0.0',
    'summary': 'Adds in the option to connect contacts to a contact indicating the familial relation between contacts.',
    'category': 'Custom',
    'author': 'Adrian',
    'license': 'LGPL-3',
    'depends': ['contacts'],
    'data': ['views/res_partner_view.xml', 
             'security/ir.model.access.csv'],
    'installable': True,
    'application': True,
    'auto_install': False
}