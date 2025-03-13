{
    "name": "Family Connections in Contacts",
    "version": "1.0.0",
    "summary": "Adds familial relationship management in Contacts.",
    "category": "Custom",
    "author": "Adrian",
    "license": "LGPL-3",
    "depends": ["contacts"],
    "data": [
        # 1) Security rules first
        "security/ir.model.access.csv",
        # 2) Child model view (for res.partner.family.relation)
        "views/res_partner_family_relation_view.xml",
        # 3) The parent form inheritance (res.partner)
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}

