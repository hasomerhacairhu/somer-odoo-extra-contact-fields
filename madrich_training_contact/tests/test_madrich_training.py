from odoo.tests import TransactionCase

class TestMadrichTraining(TransactionCase):
    def test_create_partner_with_madrich_training(self):
        """Verify that a partner can store whether they had Madrich training."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With Madrich Training',
            'madrich_training': True,
        })
        self.assertTrue(
            partner.madrich_training,
            "The contact's madrich_training field should be True."
        )
