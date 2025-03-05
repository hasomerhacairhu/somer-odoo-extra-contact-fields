from odoo.tests import TransactionCase

class TestMadrichTraining(TransactionCase):
    def test_create_partner_with_madrich_training(self):
        """Verify that a partner can store whether they had Madrich training."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With Madrich Training',
            'MadrichTraining': True,
        })
        self.assertTrue(
            partner.MadrichTraining,
            "The contact's MadrichTraining field should be True."
        )
