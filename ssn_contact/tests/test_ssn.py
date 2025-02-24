from odoo.tests import TransactionCase

class TestSSN(TransactionCase):
    def test_create_partner_with_ssn(self):
        """Check that we can store a SSN on a contact."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With SSN',
            'ssn': '123-45-6789',
        })
        self.assertEqual(partner.ssn, '123-45-6789', "SSN should be stored properly.")
