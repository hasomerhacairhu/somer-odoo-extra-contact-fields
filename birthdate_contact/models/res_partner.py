from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthdate = fields.Date(
        string='Birthday',
    )
