from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    madrich_training = fields.Boolean(
        string='Madrich Training',
        help="Indicates whether the contact had Madrich training."
    )
