from odoo.tests import TransactionCase
from datetime import date

class TestBirthDate(TransactionCase):
    def test_create_partner_with_birthdate(self):
        """Check that a partner can store a birth date."""
        partner = self.env['res.partner'].create({
            'name': 'Partner With Birthday',
            'birthdate': date(1990, 5, 15),
        })
        self.assertEqual(
            partner.birthdate,
            date(1990, 5, 15),
            "Birthdate should be stored correctly on the partner."
        )
