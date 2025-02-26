from odoo.tests import TransactionCase


class TestMembershipLevel(TransactionCase):
    def test_create_partner_with_membership_level(self):
        """Ensure we can create a Partner with a membership_level from the JSON file."""
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'membership_level': 'A',  # one of the valid JSON entries
        })
        self.assertEqual(
            partner.membership_level, 'A',
            "The new contact's membership_level should be 'A'."
        )
