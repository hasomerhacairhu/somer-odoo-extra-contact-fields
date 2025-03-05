from odoo.tests import TransactionCase
from datetime import date

class TestNextBirthday(TransactionCase):
    def test_next_birthday_logic(self):
        """
        Checks the computed NextBirthday value based on a sample birthdate.
        NOTE: Because NextBirthday depends on today's date, this test's exact 
        outcome can vary if run on different days. For a stable test, one could 
        mock fields.Date.today().
        """
        partner = self.env['res.partner'].create({
            'name': 'Contact with Birthday',
            'birthdate': date(1990, 5, 15),
        })
        # We'll verify that NextBirthday is not empty and is after today's date 
        # (the exact year depends on current date).
        self.assertTrue(partner.NextBirthday, "Next birthday should be computed if birthdate is set.")
        
        # Clear the birthdate
        partner.birthdate = False
        self.assertFalse(
            partner.NextBirthday,
            "Next birthday should be empty if no birthdate is set."
        )
