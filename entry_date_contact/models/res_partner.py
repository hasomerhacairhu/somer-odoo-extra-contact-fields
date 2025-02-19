from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    entry_date = fields.Date(
        string='Entry Date',
        help='Shows the last time the user (linked to this contact) logged in.'
    )
