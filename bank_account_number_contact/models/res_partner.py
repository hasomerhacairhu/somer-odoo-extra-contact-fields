from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_account_number = fields.Char(
        string='Bank Account Number',
        help="Stores the contact's bank account number."
    )
