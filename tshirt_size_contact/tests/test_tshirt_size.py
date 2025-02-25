from odoo.tests import TransactionCase

class TestTShirtSize(TransactionCase):
    def test_tshirt_size_selection(self):
        """Check that a contact can store a T-Shirt size from the JSON list."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With TShirtSize',
            'tshirt_size': 'XL',
        })
        self.assertEqual(
            partner.tshirt_size,
            'XL',
            "T-Shirt Size should be stored correctly as 'XL'."
        )
