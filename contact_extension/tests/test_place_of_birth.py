from odoo.tests import TransactionCase

class TestPlaceOfBirth(TransactionCase):
    def test_create_partner_with_place_of_birth(self):
        """Verify that a partner can store a place of birth."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With Place of Birth',
            'PlaceOfBirth': 'New York',
        })
        self.assertEqual(
            partner.PlaceOfBirth,
            'New York',
            "The partner's place of birth should be stored correctly."
        )
