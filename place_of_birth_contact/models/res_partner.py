from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    place_of_birth = fields.Char(
        string='Place of Birth',
        help="Stores the contact's place of birth."
    )
