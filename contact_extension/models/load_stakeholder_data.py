# load_stakeholder_data.py
from odoo import api, SUPERUSER_ID
import json
import os
import logging

_logger = logging.getLogger(__name__)

def load_stakeholder_options(env):
    """ Odoo will call this post-init hook with an `env`, not cr+registry. """
    _logger.info("==== RUNNING load_stakeholder_options HOOK ====")

    StakeholderOption = env['stakeholder.option']

    file_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'stakeholder_groups.json'
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        stakeholder_values = json.load(f)

    for val in stakeholder_values:
        existing = StakeholderOption.search([('name', '=', val)], limit=1)
        if not existing:
            StakeholderOption.create({'name': val})
    
    _logger.info("==== Finished loading %d stakeholder options ====", 
                 len(stakeholder_values))
