from odoo.tests import TransactionCase
from datetime import date

class TestExitDate(TransactionCase):
    def test_create_partner_with_exit_date(self):
        """Check that we can create a contact with an ExitDate."""
        test_partner = self.env['res.partner'].create({
            'name': 'Partner With Exit',
            'exit_date': date.today(),
        })
        self.assertIsNotNone(
            test_partner.exit_date,
            "ExitDate should be set when creating a partner."
        )
