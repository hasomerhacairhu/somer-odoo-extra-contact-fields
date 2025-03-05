from odoo.tests import TransactionCase

class TestPassportNumber(TransactionCase):
    def test_create_partner_with_passport_number(self):
        """Verify that a partner can store a PassportNumber."""
        partner = self.env['res.partner'].create({
            'name': 'Contact with Passport',
            'PassportNumber': 'AB1234567',
        })
        self.assertEqual(
            partner.PassportNumber,
            'AB1234567',
            "The partner's PassportNumber should be stored correctly."
        )
