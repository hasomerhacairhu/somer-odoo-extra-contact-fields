from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    passport_expiration_date = fields.Date(
        string='Passport Expiration Date',
        help="Stores the contact's passport expiration date."
    )
