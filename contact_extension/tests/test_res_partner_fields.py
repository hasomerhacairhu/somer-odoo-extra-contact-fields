from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date
from odoo import fields

class TestResPartnerCustomFields(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Partner = self.env['res.partner']

    def test_phone_constraint(self):
        # valid numbers pass
        p = self.Partner.create({'phone': '+1 234-567-8901'})
        self.assertEqual(p.phone, '+1 234-567-8901')
        # invalid numbers raise
        with self.assertRaises(ValidationError):
            self.Partner.create({'phone': 'BADPHONE'})

    def test_onchange_exit_date_clears_reason(self):
        p = self.Partner.new({'ExitDate': date.today(), 'ExitReason': 'foo'})
        # Simulate user clearing the date
        p.ExitDate = False
        p._onchange_exit_date()
        self.assertEqual(p.ExitReason, '')

    def test_compute_age_and_next_birthday(self):
        bday = date(2000, 5, 1)
        today = date.today()
        p = self.Partner.create({'BirthDate': bday})
        # Age
        expected_age = today.year - 2000 - ((today.month, today.day) < (5,1))
        self.assertEqual(p.Age, expected_age)
        # NextBirthday
        upcoming = date(
            today.year + (today >= date(today.year,5,1)),
            5,1
        )
        self.assertEqual(p.NextBirthday, upcoming)

    def test_update_age_and_next_birthday_cron(self):
        # create two records: one with birthdate, one without
        bday = date(1990, 1, 1)
        r1 = self.Partner.create({'BirthDate': bday})
        r2 = self.Partner.create({'BirthDate': False})
        # call cron
        self.Partner.update_age_and_next_birthday()
        # r1 should have Age and NextBirthday set
        self.assertTrue(r1.Age > 0)
        self.assertIsNot(r1.NextBirthday, False)
        # r2 should remain at default 0 / False
        self.assertEqual(r2.Age, 0)
        self.assertFalse(r2.NextBirthday)

    def test_selection_fields_have_expected_values(self):
        # MembershipLevel
        opts = [val for (val,_) in self.Partner._fields['MembershipLevel'].selection]
        self.assertIn('A', opts)       # etc., depending on your JSON
        # TShirtSize
        sizes = [val for (val,_) in self.Partner._fields['TShirtSize'].selection]
        self.assertIn('M', sizes)

    def test_other_custom_fields_roundtrip(self):
        # you can loop through simple Char/Bool fields
        test_data = {
            'Nickname': 'Nick',
            'IDNumber': '1234',
            'SSN': '987-65-4321',
            'TaxID': 'TAX-ID',
            'PassportNumber': 'P123',
            'BankAccountNumber': 'BE123',
            'PlaceOfBirth': 'Budapest',
            'IsActive': True,
            'IsVaccinated': False,
            'MadrichTraining': True,
        }
        p = self.Partner.create(test_data)
        for field, value in test_data.items():
            self.assertEqual(getattr(p, field), value)
