from odoo.tests import TransactionCase
from datetime import date

class TestExitReason(TransactionCase):
    def test_exit_reason_hidden_without_exit_date(self):
        # Create a partner with no exit_date. Even if an exit_reason is provided,
        # the onchange should clear it.
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'ExitDate': False,
            'ExitReason': 'Some reason'
        })
        partner._onchange_exit_date()  # simulate onchange trigger
        self.assertEqual(partner.ExitReason, '', 
                         "Exit reason should be cleared when exit_date is not provided.")

    def test_exit_reason_visible_with_exit_date(self):
        # Create a partner with an exit_date. The exit_reason should remain as set.
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'ExitDate': date(2025, 2, 25),
            'ExitReason': 'Resigned'
        })
        self.assertEqual(partner.ExitReason, 'Resigned', 
                         "Exit reason should remain editable when exit_date is provided.")
