from odoo.tests.common import TransactionCase
from odoo import fields

class TestResPartnerAge(TransactionCase):
    def test_age_computation_from_birthdate(self):
        """
        Test that Age is correctly computed from BirthDate.
        """
        partner = self.env['res.partner'].create({
            'name': 'Partner With Known Age',
            'BirthDate': '2000-01-01'
        })

        # Force recompute (usually automatic, but explicit for clarity)
        partner._computeAge()

        # Calculate expected age
        today = fields.Date.today()
        days_diff = (today - fields.Date.to_date('2000-01-01')).days
        expected_age = days_diff // 365

        self.assertEqual(
            partner.Age,
            expected_age,
            "Age should match the difference in years between BirthDate and today."
        )

    def test_age_zero_for_null_birthdate(self):
        """
        Test that Age is 0 if BirthDate isn't set.
        """
        partner = self.env['res.partner'].create({'name': 'Partner Without Birthdate'})
        partner._computeAge()
        self.assertEqual(
            partner.Age,
            0,
            "Age should be 0 when BirthDate is not provided."
        )
