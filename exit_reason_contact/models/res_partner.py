from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    exit_reason = fields.Text(
        string='Exit Reason',
        help='Reason for the user\'s exit. Only visible if exit_date is set.'
    )
