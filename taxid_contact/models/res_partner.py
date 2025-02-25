from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tax_id = fields.Char(
        string='Tax ID',
        help='Tax Identification Number for this contact.'
    )
