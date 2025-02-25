from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_vaccinated = fields.Boolean(
        string='Is Vaccinated',
        help="Indicates whether the contact is vaccinated."
    )
