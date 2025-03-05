from odoo import api, fields, models
from datetime import datetime
import os
import json

# Dynamically load the membership options from our JSON file
CONFIG_PATH_1 = os.path.join(
    os.path.dirname(__file__),
    '..',  # up one folder
    'data',
    'membership_levels.json'
)

with open(CONFIG_PATH_1, 'r', encoding='utf-8') as f:
    MEMBERSHIP_OPTIONS = json.load(f)

# Convert ["A", "B", "C"] into [(“A”, “A”), (“B”, “B”), (“C”, “C”)]
MEMBERSHIP_SELECTION = [(val, val) for val in MEMBERSHIP_OPTIONS]

# Dynamically load the stakeholder options from our JSON file
CONFIG_PATH_2 = os.path.join(
    os.path.dirname(__file__),
    '..',  # up one folder
    'data',
    'stakeholder_groups.json'
)

with open(CONFIG_PATH_2, 'r', encoding='utf-8') as f:
    STAKEHOLDER_OPTIONS = json.load(f)

STAKEHOLDER_SELECTION = [(val, val) for val in STAKEHOLDER_OPTIONS]



class ResPartner(models.Model):
    _inherit = 'res.partner'

    EntryDate = fields.Date(string='Entry Date', 
        help='Shows the last time the user (linked to this contact) logged in.')
    ExitDate = fields.Date(
        string='Exit Date',
        help='Stores the date on which this contact/user exited.')
    ExitReason = fields.Text()
    @api.onchange('ExitDate')
    def _onchange_exit_date(self):
        # If ExitDate is not provided, clear ExitReason.
        if not self.ExitDate:
            self.ExitReason = ''
    MembershipLevel = fields.Selection(
        selection=MEMBERSHIP_SELECTION,
        string='Membership Level')
    BirthDate = fields.Date(string='Birthdate')
    Age = fields.Integer(string='Age', compute='_computeAge', 
        store=True)
    @api.depends('BirthDate')
    def _computeAge(self):
        today = fields.Date.today()
        for records in self:
            if records.BirthDate:
                days_diff = (today - records.BirthDate).days
                records.Age = days_diff // 365
            else:
                records.Age = 0
    StakeholderGroup = fields.Selection(selection=STAKEHOLDER_SELECTION,
        string='Stakeholder Group')



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
