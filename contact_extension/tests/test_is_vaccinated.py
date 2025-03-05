from odoo.tests import TransactionCase

class TestIsVaccinated(TransactionCase):
    def test_create_partner_with_is_vaccinated(self):
        """Verify that a partner can store a boolean indicating vaccination status."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With Vaccination Status',
            'IsVaccinated': True,
        })
        self.assertTrue(
            partner.IsVaccinated,
            "The contact's IsVaccinated field should be True."
        )
