from odoo import models, fields

class StakeholderGroup(models.Model):
    _name = 'stakeholder.group'
    _description = 'Stakeholder Group'

    name = fields.Char(required=True, translate=True)
