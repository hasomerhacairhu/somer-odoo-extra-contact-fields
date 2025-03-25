import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date
import os
import json

# Dynamically load the membership options from our JSON file
CONFIG_PATH_MEMBERSHIP = os.path.join(
    os.path.dirname(__file__),
    '..',  # up one folder
    'data',
    'membership_levels.json'
)

with open(CONFIG_PATH_MEMBERSHIP, 'r', encoding='utf-8') as f:
    MEMBERSHIP_OPTIONS = json.load(f)

# Convert ["A", "B", "C"] into [(“A”, “A”), (“B”, “B”), (“C”, “C”)]
MEMBERSHIP_SELECTION = [(val, val) for val in MEMBERSHIP_OPTIONS]

# Load T-shirt size options from tshirt_sizes.json at import time
CONFIG_PATH_TSHIRT = os.path.join(
    os.path.dirname(__file__),
    '..',  # up one directory
    'data',
    'tshirt_sizes.json'
)

with open(CONFIG_PATH_TSHIRT, 'r', encoding='utf-8') as f:
    TSHIRT_SIZE_OPTIONS = json.load(f)

# Convert ["XS","S","M","L","XL","XXL","3XL","4XL","5XL"] to:
# [("XS","XS"),("S","S"),("M","M"), ... ]
TSHIRT_SIZE_SELECTION = [(size, size) for size in TSHIRT_SIZE_OPTIONS]

# Example regex for Hungarian phone: +36 XX 123 4567 or 06 XX 123 4567, etc.
# Adjust spacing/length if needed.
HUNGARIAN_PHONE_REGEX = re.compile(r'^(?:\+36|06)\s?\d{1,2}\s?\d{3,4}\s?\d{3,4}$')

# ----------------------------
#  Model to store Stakeholder Options
# ----------------------------
class StakeholderOption(models.Model):
    _name = 'stakeholder.option'
    _description = 'Stakeholder Options'

    name = fields.Char(string='Name', required=True, index=True)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    title = fields.Many2one(
    'res.partner.title',
    string="Title"
)

    #NOT USED/DISPLAYED because there is some error when trying to 
    # make it a non-selection type of field due to 
    # overriding issues with the built-in 
    # 'function' (Job Position field)
    function = fields.Selection(selection=[('job', 'Job')], string='Job Position')
    
    phone = fields.Char(string='Phone')
    @api.constrains('phone')
    def _check_phone_hungarian_format(self):
        for rec in self:
            # Skip empty phone fields
            if not rec.phone:
                continue
            # If the phone doesn't match our Hungarian pattern, raise an error
            if not HUNGARIAN_PHONE_REGEX.match(rec.phone):
                raise ValidationError(
                    "Invalid phone format. Please enter a valid Hungarian phone number, "
                    "for example: +36 30 123 4567 or 06 70 123 4567."
                )

    email = fields.Char(string='Email')

    website = fields.Char(string='Website')
    
    EntryDate = fields.Date(string='Entry Date'
        , help = 'A mozgalomba való belépés dátuma')
    
    ExitDate = fields.Date(string='Exit Date'
        , help = 'A mozgalomból való kilépés dátuma')
    
    ExitReason = fields.Char(string='Exit Reason'
        , help = 'A mozgalomból való kilépés oka')
    @api.onchange('ExitDate')
    def _onchange_exit_date(self):
        # If ExitDate is not provided, clear ExitReason.
        if not self.ExitDate:
            self.ExitReason = ''
    
    MembershipLevel = fields.Selection(
        selection=MEMBERSHIP_SELECTION,
        string='Membership Level')
    
    BirthDate = fields.Date(string='Date of Birth')
    
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
    
    StakeholderGroup = fields.Many2many(
        comodel_name='stakeholder.option',
        string='Stakeholder Group'
    )
    
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
    
    IsActive = fields.Boolean(string='Is Active', 
        help='Indicates whether the contact is an active member.')
    
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

