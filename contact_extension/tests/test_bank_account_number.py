from odoo.tests import TransactionCase

class TestBankAccountNumber(TransactionCase):
    def test_create_partner_with_bank_account_number(self):
        """Verify that a partner can store a bank account number."""
        partner = self.env['res.partner'].create({
            'name': 'Contact With Bank Account',
            'BankAccountNumber': '123456789ABC',
        })
        self.assertEqual(
            partner.BankAccountNumber,
            '123456789ABC',
            "The partner's bank account number should be stored correctly."
        )
