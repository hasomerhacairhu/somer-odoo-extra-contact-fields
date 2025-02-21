from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    stakeholder_group_ids = fields.Many2many(
        'stakeholder.group',
        string='Stakeholder Group',
        help='Select one or more stakeholder groups for this contact.'
    )
