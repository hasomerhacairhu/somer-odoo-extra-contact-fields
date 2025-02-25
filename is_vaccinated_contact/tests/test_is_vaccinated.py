from odoo.tests import TransactionCase

class TestIsVaccinated(TransactionCase):
    def test_create_partner_with_is_vaccinated(self):
        """Verify that a partner can store a boolean indicating vaccination status."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With Vaccination Status',
            'is_vaccinated': True,
        })
        self.assertTrue(
            partner.is_vaccinated,
            "The contact's is_vaccinated field should be True."
        )
