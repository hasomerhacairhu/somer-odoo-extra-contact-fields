from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    exit_date = fields.Date(
        string='Exit Date',
        help='Stores the date on which this contact/user exited.'
    )
