from odoo.tests import TransactionCase
from odoo import fields
from datetime import datetime, timedelta

class TestEntryDateContact(TransactionCase):
    def setUp(self):
        super(TestEntryDateContact, self).setUp()
        # Create a test user with a related partner.
        self.test_user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser@example.com',
        })

    def test_entry_date_updates_on_login(self):
        """
        When the user's login_date is written, the partner's entry_date
        should be updated to that date (date portion only).
        """
        # Simulate a login by writing 'login_date' to the user.
        fake_login_datetime = datetime.now() - timedelta(days=1)
        self.test_user.write({
            'login_date': fake_login_datetime,
        })

        # The partner's entry_date should match the date portion of login_date.
        expected_date = fields.Date.to_date(fake_login_datetime)
        self.assertEqual(
            self.test_user.partner_id.entry_date,
            expected_date,
            "Partner's entry_date should be set to the date portion of the user's login_date."
        )

    def test_entry_date_cleared_if_no_login_date(self):
        """
        If the user's login_date is set to False, the partner's entry_date
        should be cleared as well.
        """
        # First, set a login_date
        self.test_user.write({'login_date': datetime.now()})
        self.assertIsNotNone(self.test_user.partner_id.entry_date)

        # Now clear it
        self.test_user.write({'login_date': False})
        self.assertFalse(
            self.test_user.partner_id.entry_date,
            "Partner's entry_date should be cleared if the user's login_date is set to False."
        )
