from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nickname = fields.Char(
        string='Nickname',
        help='An optional nickname for this contact.'
    )
