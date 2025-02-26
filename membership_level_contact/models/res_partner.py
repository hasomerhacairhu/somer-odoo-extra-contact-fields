import os
import json
from odoo import models, fields

# Dynamically load the membership options from our JSON file
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',  # up one folder
    'data',
    'membership_levels.json'
)

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    MEMBERSHIP_OPTIONS = json.load(f)

# Convert ["A", "B", "C"] into [(“A”, “A”), (“B”, “B”), (“C”, “C”)]
MEMBERSHIP_SELECTION = [(val, val) for val in MEMBERSHIP_OPTIONS]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    membership_level = fields.Selection(
        selection=MEMBERSHIP_SELECTION,
        string='Membership Level',
        help='Choose the membership level for this contact.'
    )
