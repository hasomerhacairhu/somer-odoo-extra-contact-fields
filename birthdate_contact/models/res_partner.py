from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthdate = fields.Date(
        string='Birthday',
        help='Stores the birthday of this contact as a date.'
    )
