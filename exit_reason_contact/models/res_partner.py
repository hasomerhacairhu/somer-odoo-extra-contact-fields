from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    exit_reason = fields.Text(
        string='Exit Reason',
        help="Reason for exit. This field is only visible when Exit Date is provided."
    )

    @api.onchange('exit_date')
    def _onchange_exit_date(self):
        # If exit_date is not provided, clear exit_reason.
        if not self.exit_date:
            self.exit_reason = ''
