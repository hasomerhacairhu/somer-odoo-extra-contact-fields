from odoo.tests import TransactionCase
from datetime import date

class TestPassportExpirationDate(TransactionCase):
    def test_create_partner_with_passport_expiration_date(self):
        """Verify that a partner can store a passport expiration date."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With Passport Expiration',
            'passport_expiration_date': date(2030, 12, 31),
        })
        self.assertEqual(
            partner.passport_expiration_date,
            date(2030, 12, 31),
            "The partner's passport expiration date should be stored correctly."
        )
