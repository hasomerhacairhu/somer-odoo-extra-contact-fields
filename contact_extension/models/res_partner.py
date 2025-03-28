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


# Accepts an optional '+' at the start, then any combination of digits, spaces, dashes, periods, and parentheses.
# The pattern requires at least 7 characters and enforces a maximum of 15 digits (ignoring formatting characters)
# to comply with the ITU-T E.164 standard for international phone numbers.
PHONE_REGEX = re.compile(
    r'^(?=(?:\D*\d){7,15}\D*$)\+?[0-9\-\.\s\(\)]+$'
)


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
    def _check_phone_format(self):
        for rec in self:
            # Skip empty phone fields
            if not rec.phone:
                continue
            # If the phone doesn't match our global pattern, raise an error
            if not PHONE_REGEX.match(rec.phone):
                raise ValidationError(
                    "Invalid phone format. Please enter a valid phone number: Only digits, spaces, dashes, periods, "
                    "parentheses, and an optional leading '+' are allowed. "
                    "The length of the phone number has to be between 7-15 digits long, "
                    "not including other characters and spaces"
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
    
    Age = fields.Integer(string='Age', compute='_compute_age', 
        store=True)
    @api.depends('BirthDate')
    def _compute_age(self):
        for rec in self:
            if rec.BirthDate:
                today = fields.Date.today()  # Used only for calculation, not as a dependency
                # Calculate the difference in years in a simple way
                rec.Age = today.year - rec.BirthDate.year - (
                    (today.month, today.day) < (rec.BirthDate.month, rec.BirthDate.day)
                )
            else:
                rec.Age = 0

    NextBirthday = fields.Date(string='Next Birthday',
        compute='_compute_next_birthday',
        help="Shows the next upcoming birthday, based on the Birthday field.")
    @api.depends('BirthDate')
    def _compute_next_birthday(self):
        for rec in self:
            if not rec.BirthDate:
                rec.NextBirthday = False
            else:
                today = fields.Date.today()  # Used only for calculation
                bday_month = rec.BirthDate.month
                bday_day = rec.BirthDate.day
                current_year_bday = date(today.year, bday_month, bday_day)
                if current_year_bday <= today:
                    rec.NextBirthday = date(today.year + 1, bday_month, bday_day)
                else:
                    rec.NextBirthday = current_year_bday

    @api.model
    def update_age_and_next_birthday(self):
        """Scheduled method to update Age and NextBirthday for all records.
        This should be set up as a daily cron job."""
        today = fields.Date.today()
        partners = self.search([('BirthDate', '!=', False)])
        for partner in partners:
            # Calculate age
            new_age = today.year - partner.BirthDate.year - (
                (today.month, today.day) < (partner.BirthDate.month, partner.BirthDate.day)
            )
            # Calculate next birthday
            bday_month = partner.BirthDate.month
            bday_day = partner.BirthDate.day
            current_year_bday = date(today.year, bday_month, bday_day)
            new_next_bday = date(today.year + 1, bday_month, bday_day) if current_year_bday <= today else current_year_bday

            partner.write({'Age': new_age, 'NextBirthday': new_next_bday})
    
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
    
