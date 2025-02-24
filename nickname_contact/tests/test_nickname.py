from odoo.tests import TransactionCase

class TestNickname(TransactionCase):
    def test_create_partner_with_nickname(self):
        """Ensure a partner can be created with a nickname."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With Nickname',
            'nickname': 'Nick',
        })
        self.assertEqual(partner.nickname, 'Nick', "Nickname should be stored properly.")
