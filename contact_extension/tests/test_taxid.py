from odoo.tests import TransactionCase

class TestTaxID(TransactionCase):
    def test_create_partner_with_taxid(self):
        """Verify that a partner can store a TaxID."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With TaxID',
            'TaxID': 'TAX-12345',
        })
        self.assertEqual(
            partner.TaxID,
            'TAX-12345',
            "The partner's TaxID should be stored correctly."
        )
