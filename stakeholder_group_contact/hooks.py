import json
import os
from odoo import api, SUPERUSER_ID

def post_init_hook(env):
    cr = env.cr
    group_model = env['stakeholder.group']
    # Path relative to the 'hooks.py' file
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'stakeholder_groups.json')
    if not os.path.exists(json_path):
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        group_names = json.load(f)

    for name in group_names:
        existing = group_model.search([('name', '=', name)], limit=1)
        if not existing:
            group_model.create({'name': name})
