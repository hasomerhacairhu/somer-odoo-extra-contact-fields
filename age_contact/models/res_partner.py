from datetime import date
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
    )

    @api.depends('birthdate')
    def _compute_age(self):
        today = fields.Date.today()
        for partner in self:
            if partner.birthdate:
                years = today.year - partner.birthdate.year
                if (today.month, today.day) < (partner.birthdate.month, partner.birthdate.day):
                    years -= 1
                partner.age = years
            else:
                partner.age = -1  # Sentinel value for no birthday
