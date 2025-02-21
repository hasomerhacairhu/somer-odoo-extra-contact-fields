from odoo.tests import TransactionCase

class TestStakeholderGroup(TransactionCase):
    def test_assign_multiple_groups(self):
        # Get some existing stakeholder groups (loaded from JSON at install)
        group_model = self.env['stakeholder.group']
        sample_groups = group_model.search([], limit=3)
        # Create a contact and assign multiple stakeholder groups
        partner = self.env['res.partner'].create({
            'name': 'Test Partner Multiple Groups',
            'stakeholder_group_ids': [(6, 0, sample_groups.ids)]
        })
        self.assertEqual(
            set(partner.stakeholder_group_ids.ids),
            set(sample_groups.ids),
            "The partner should have multiple stakeholder groups assigned."
        )
