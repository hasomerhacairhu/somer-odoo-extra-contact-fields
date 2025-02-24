from odoo.tests import TransactionCase

class TestIDNumber(TransactionCase):
    def test_create_partner_with_idnumber(self):
        """Verify that we can create a partner with an ID number."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With ID',
            'id_number': 'ABC123XYZ',
        })
        self.assertEqual(
            partner.id_number,
            'ABC123XYZ',
            "The partner's IDNumber should be stored correctly."
        )
