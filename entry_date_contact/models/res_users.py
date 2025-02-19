from odoo import models, fields, api
from datetime import datetime

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Whenever the built-in 'login_date' changes, we push that date to the related partner.
    @api.model
    def write(self, vals):
        res = super(ResUsers, self).write(vals)

        if 'login_date' in vals:
            for user in self:
                if user.partner_id:
                    # login_date is a datetime; convert to date if you want only the date part.
                    if user.login_date:
                        user.partner_id.entry_date = fields.Date.to_date(user.login_date)
                    else:
                        user.partner_id.entry_date = False
        return res
