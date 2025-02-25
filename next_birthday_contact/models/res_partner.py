from datetime import date
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    next_birthday = fields.Date(
        string='Next Birthday',
        compute='_compute_next_birthday',
        help="Shows the next upcoming birthday date, based on the Birthday field."
    )

    @api.depends('birthdate')
    def _compute_next_birthday(self):
        for partner in self:
            if not partner.birthdate:
                partner.next_birthday = False
            else:
                today = fields.Date.today()
                # Convert to datetime.date for month/day comparison
                bday_month = partner.birthdate.month
                bday_day = partner.birthdate.day

                current_year_bday = date(today.year, bday_month, bday_day)
                if current_year_bday < today:
                    # If birthday already happened this year, use next year
                    partner.next_birthday = date(today.year + 1, bday_month, bday_day)
                else:
                    # Otherwise, use current year
                    partner.next_birthday = current_year_bday
