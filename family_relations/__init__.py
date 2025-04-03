from . import models

import odoo
from odoo import release

if release.version_info[0] < 16:
    raise ImportError("This module requires Odoo 16 or higher.")
