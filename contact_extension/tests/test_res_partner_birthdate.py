from odoo.tests.common import TransactionCase

class TestResPartnerBirthDate(TransactionCase):
    def test_birthdate_set_correctly(self):
        """
        Test that setting BirthDate on a partner works
        and that the field can be read back as expected.
        """
        partner = self.env['res.partner'].create({
            'name': 'Partner With Birthday',
            'BirthDate': '2000-01-01',
        })
        self.assertEqual(
            str(partner.BirthDate),
            '2000-01-01',
            "BirthDate should match what was set during creation."
        )

    def test_birthdate_unset_should_be_false(self):
        """
        Test that if BirthDate is not set, the field should remain False / None.
        """
        partner = self.env['res.partner'].create({'name': 'Partner Without Birthdate'})
        self.assertFalse(
            partner.BirthDate,
            "BirthDate should be False (or None) when not provided."
        )
