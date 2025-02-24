from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_number = fields.Char(
        string='ID Number',
        help='A string to store the contact\'s ID number.'
    )
