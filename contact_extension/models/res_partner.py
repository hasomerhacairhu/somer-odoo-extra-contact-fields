from odoo import api, fields, models
from datetime import date
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


# Load T-shirt size options from tshirt_sizes.json at import time
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',  # up one directory
    'data',
    'tshirt_sizes.json'
)

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    TSHIRT_SIZE_OPTIONS = json.load(f)

# Convert ["XS","S","M","L","XL","XXL","3XL","4XL","5XL"] to:
# [("XS","XS"),("S","S"),("M","M"), ... ]
TSHIRT_SIZE_SELECTION = [(size, size) for size in TSHIRT_SIZE_OPTIONS]



class ResPartner(models.Model):
    _inherit = 'res.partner'

    EntryDate = fields.Date(string='Entry Date', 
        help='Shows the last time the user (linked to this contact) logged in.')
    
    ExitDate = fields.Date(
        string='Exit Date',
        help='Stores the date on which this contact/user exited.')
    
    ExitReason = fields.Char(string='Exit Reason')
    @api.onchange('ExitDate')
    def _onchange_exit_date(self):
        # If ExitDate is not provided, clear ExitReason.
        if not self.ExitDate:
            self.ExitReason = ''
    
    MembershipLevel = fields.Selection(
        selection=MEMBERSHIP_SELECTION,
        string='Membership Level')
    
    BirthDate = fields.Date(string='Birthday')
    
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
    
    Nickname = fields.Char(string='Nickname')
    
    IDNumber = fields.Char(string='ID Number')
    
    SSN = fields.Char(string='SSN', 
        help='Contact\'s Social Security Number.')
    
    TShirtSize = fields.Selection(selection=TSHIRT_SIZE_SELECTION,
        string='T-Shirt Size',
        help='Dropdown storing the T-shirt size of the contact.')
    
    TaxID = fields.Char(string='Tax ID',
        help='Tax Identification Number for this contact.')
    
    PassportNumber = fields.Char(string='Passport Number')
    
    PassportExpirationDate = fields.Date(string='Passport Expiration Date')
    
    BankAccountNumber = fields.Char(string='Bank Account Number')
    
    PlaceOfBirth = fields.Char(string='Place of Birth')
    
    IsVaccinated = fields.Boolean(string='Is Vaccinated',
        help="Indicates whether the contact is vaccinated.")
    
    MadrichTraining = fields.Boolean(string='Madrich Training',
        help="Indicates whether the contact had Madrich training.")
    
    NextBirthday = fields.Date(string='Next Birthday',
        compute='_compute_next_birthday',
        help="Shows the next upcoming birthday, based on the Birthday field.")
    @api.depends('BirthDate')
    def _compute_next_birthday(self):
        for partner in self:
            if not partner.BirthDate:
                partner.NextBirthday = False
            else:
                today = fields.Date.today()
                # Convert to datetime.date for month/day comparison
                bday_month = partner.BirthDate.month
                bday_day = partner.BirthDate.day

                current_year_bday = date(today.year, bday_month, bday_day)
                if current_year_bday < today:
                    # If birthday already happened this year, use next year
                    partner.NextBirthday = date(today.year + 1, bday_month, bday_day)
                else:
                    # Otherwise, use current year
                    partner.NextBirthday = current_year_bday



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
