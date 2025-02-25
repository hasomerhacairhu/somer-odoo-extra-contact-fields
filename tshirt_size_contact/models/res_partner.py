import os
import json
from odoo import models, fields

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

    tshirt_size = fields.Selection(
        selection=TSHIRT_SIZE_SELECTION,
        string='T-Shirt Size',
        help='Dropdown storing the T-shirt size of the contact.'
    )
