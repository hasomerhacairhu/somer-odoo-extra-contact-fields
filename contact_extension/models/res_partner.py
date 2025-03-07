from odoo import api, fields, models
from datetime import date
import os
import json

# TODO - születésnap, stakeholder, entry, exit (csak, ha entry megvan)
# , nickname, membership level, 
# Egy új tabot hozz létre a többinek: SSN, TAX, Bool értékek stb... 
# logikus csoportosítás!

# +TODO - Változó nevek legyenek intuitívek!

# TODO - Családi kapcsolatok: Odoo részek újrafelhasználásával: 
# LIST VIEW (- Meglévő táblázat vezérlőt próbáld újrahasználni - list_view): 
# 3 oszlop: név, legördülő menü: kapcsolódás fajtái vannak vagy egyéb, harmadik pedig egy link a rokon profiljára, 
# törlés, KÖLCSÖNÖS MEGJELENÍTÉS

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


# Dynamically load the stakeholder options from our JSON file
CONFIG_PATH_STAKEHOLDER = os.path.join(
    os.path.dirname(__file__),
    '..',  # up one folder
    'data',
    'stakeholder_groups.json'
)

with open(CONFIG_PATH_STAKEHOLDER, 'r', encoding='utf-8') as f:
    STAKEHOLDER_OPTIONS = json.load(f)

STAKEHOLDER_SELECTION = [(val, val) for val in STAKEHOLDER_OPTIONS]


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



class ResPartner(models.Model):
    _inherit = 'res.partner'

    EntryDate = fields.Date(string='Entry Date'
        , help = 'A mozgalomba való belépés dátuma')
    
    ExitDate = fields.Date(string='Exit Date'
        , help = 'A mozgalomból való kilépés dátuma')
    
    # +TODO - todo note: EntryDate-nél, hogy mikor lépett be a mozgalomba!
    # +TODO - todo note: ExitReason-nél tűnjön el a field, ha nincs ExitDate
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
    
    BirthDate = fields.Date(string='Birthday')
    
    # +TODO - todo note: Backend-en vagy Frontend-en számloja? 
    # A válasz: A Backend-en számolódik, 
    # a kódon belül mindig újraszámolódik az @api.depends-nek köszönhetően 
    # és a Frontend-en csak szimplán megjelenik a böngészőn
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

