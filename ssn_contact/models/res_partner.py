from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ssn = fields.Char(
        string='SSN',
        help='Contact\'s Social Security Number.'
    )
