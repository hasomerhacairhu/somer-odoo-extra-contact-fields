from odoo.tests import TransactionCase
from datetime import date

class TestExitReason(TransactionCase):
    def test_exit_reason_logic(self):
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'exit_date': date.today(),
            'exit_reason': 'Retired',
        })
        self.assertEqual(partner.exit_reason, 'Retired', "ExitReason should be saved.")
        partner.exit_date = False
        partner.exit_reason = 'Should still store but the UI is hidden.'
        self.assertEqual(partner.exit_reason, 'Should still store but the UI is hidden.')
