from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    passport_number = fields.Char(
        string='Passport Number',
    )
