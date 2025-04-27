from odoo.tests import common

class TestPartnerFamilyRelation(common.TransactionCase):

    def setUp(self):
        super(TestPartnerFamilyRelation, self).setUp()
        # Create some test partners
        self.partner_a = self.env['res.partner'].create({'name': 'Partner A'})
        self.partner_b = self.env['res.partner'].create({'name': 'Partner B'})
    
    def test_01_create_reciprocal(self):
        """
        Test that creating a family relation automatically creates
        its reciprocal record using our new relationship map.
        """
        # Example: "parent" -> reciprocal "child"
        relation = self.env['res.partner.family.relation'].create({
            'partner_id': self.partner_a.id,
            'related_partner_id': self.partner_b.id,
            'relationship_type': 'parent',
            'comment': 'Testing comment'
        })

        # The reciprocal should have been created
        reciprocal = self.env['res.partner.family.relation'].search([
            ('partner_id', '=', self.partner_b.id),
            ('related_partner_id', '=', self.partner_a.id),
        ], limit=1)

        self.assertTrue(reciprocal, "Reciprocal relation should have been created.")
        self.assertEqual(reciprocal.relationship_type, 'child',
                         "Expected the reciprocal type to be 'child'.")
        self.assertEqual(reciprocal.comment, 'Testing comment',
                         "Expected the reciprocal to copy the comment.")

    def test_02_write_reciprocal(self):
        """
        Test that writing changes to relationship_type or comment
        on one record also updates the reciprocal record.
        """
        # Start with "grandparent" -> reciprocal "grandchild"
        relation = self.env['res.partner.family.relation'].create({
            'partner_id': self.partner_a.id,
            'related_partner_id': self.partner_b.id,
            'relationship_type': 'grandparent'
        })

        reciprocal = self.env['res.partner.family.relation'].search([
            ('partner_id', '=', self.partner_b.id),
            ('related_partner_id', '=', self.partner_a.id),
        ], limit=1)
        self.assertEqual(reciprocal.relationship_type, 'grandchild',
                         "Initial reciprocal should be 'grandchild'.")

        # Now update the original record to "other" plus a new comment
        relation.write({
            'relationship_type': 'other',
            'comment': 'New comment for other relationship'
        })

        # Refresh the reciprocal
        reciprocal.invalidate_cache()
        reciprocal.read(['relationship_type', 'comment'])

        # "other" -> reciprocal "other"
        self.assertEqual(reciprocal.relationship_type, 'other',
            "Reciprocal relationship should update to 'other'.")
        self.assertEqual(reciprocal.comment, 'New comment for other relationship',
            "Reciprocal comment should mirror the original record's comment.")

    def test_03_unlink_reciprocal(self):
        """
        Test that unlinking one side removes the reciprocal record.
        We'll use 'sibling' -> 'sibling' as an example of symmetrical.
        """
        relation = self.env['res.partner.family.relation'].create({
            'partner_id': self.partner_a.id,
            'related_partner_id': self.partner_b.id,
            'relationship_type': 'sibling'
        })

        reciprocal = self.env['res.partner.family.relation'].search([
            ('partner_id', '=', self.partner_b.id),
            ('related_partner_id', '=', self.partner_a.id),
        ], limit=1)

        self.assertEqual(reciprocal.relationship_type, 'sibling',
                         "Reciprocal side should be 'sibling' for symmetrical relationships.")

        # Unlink the original record
        relation.unlink()

        # The reciprocal record should also be gone
        self.assertFalse(reciprocal.exists(),
            "Unlinking one side should also remove the reciprocal record.")
