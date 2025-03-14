from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # One2many to store this partner's family relationships
    relation_ids = fields.One2many(
        'res.partner.family.relation',
        'partner_id',
        string='Family Connections'
    )

class ResPartnerFamilyRelation(models.Model):
    _name = 'res.partner.family.relation'
    _description = 'Family Relation Between Two Contacts'

    partner_id = fields.Many2one(
        'res.partner',
        string='Main Contact',
        required=True,
        ondelete='cascade'
    )
    related_partner_id = fields.Many2one(
        'res.partner',
        string='Related Contact',
        required=True,
        ondelete='cascade'
    )
    relationship_type = fields.Selection(
        [
        # Parent/Child
        ('parent', 'Parent'),
        ('child', 'Child'),
        ('step_parent', 'Step-parent'),
        ('step_child', 'Step-child'),

        # Siblings
        ('sibling', 'Sibling'),
        ('half_sibling', 'Half-sibling'),
        ('step_sibling', 'Step-sibling'),

        # Spouse / Engagement
        ('spouse', 'Spouse'),
        ('ex_spouse', 'Ex-Spouse'),
        ('fiance', 'Fiancé(e)'),

        # Grandparent / Grandchild
        ('grandparent', 'Grandparent'),
        ('grandchild', 'Grandchild'),

        # Aunt/Uncle vs. Niece/Nephew
        ('aunt_or_uncle', 'Aunt/Uncle'),
        ('niece_or_nephew', 'Niece/Nephew'),

        # Cousin
        ('cousin', 'Cousin'),

        # In-laws
        ('parent_in_law', 'Parent-in-law'),
        ('child_in_law', 'Child-in-law'),
        ('brother_in_law', 'Brother-in-law'),
        ('sister_in_law', 'Sister-in-law'),
        ],
        string='Relationship',
        required=True,
    )

    # -------------------------------------------------------------------------
    #  Reciprocal logic
    # -------------------------------------------------------------------------

    @api.model
    def create(self, vals):
        """Override create to ensure reciprocal relationship gets created."""
        record = super().create(vals)

        # If we’re creating from the user side, create a reciprocal relation
        # for the 'other' partner as well, unless we detect a reciprocal
        # creation is already in progress (avoid infinite recursion).
        if not self.env.context.get('skip_reciprocal'):
            reciprocal_type = record._get_reciprocal_relationship_type(
                record.relationship_type
            )
            if reciprocal_type:
                # Create the 'opposite' side, passing skip_reciprocal=True to avoid loops
                self.with_context(skip_reciprocal=True).create(
                    {
                        'partner_id': record.related_partner_id.id,
                        'related_partner_id': record.partner_id.id,
                        'relationship_type': reciprocal_type,
                    },
                )

        return record

    def write(self, vals):
        """Override write to update reciprocal records if relationship_type changes."""
        res = super().write(vals)

        # If relationship_type changes, we need to update the reciprocal side
        if 'relationship_type' in vals:
            for rec in self:
                if not self.env.context.get('skip_reciprocal'):
                    # Find the reciprocal record on the related partner, if any
                    reciprocal_rel = self.search([
                        ('partner_id', '=', rec.related_partner_id.id),
                        ('related_partner_id', '=', rec.partner_id.id),
                    ], limit=1)
                    if reciprocal_rel:
                        # Compute new reciprocal
                        new_reciprocal_type = rec._get_reciprocal_relationship_type(
                            rec.relationship_type
                        )
                        # Update that side
                        reciprocal_rel.with_context(skip_reciprocal=True).write({
                            'relationship_type': new_reciprocal_type
                        })

        return res

    def unlink(self):
        """Override unlink to remove the reciprocal relation from the other side."""
        reciprocal_records = self.env['res.partner.family.relation']
        for rec in self:
            # Find the reciprocal record on the related partner
            recp = self.search([
                ('partner_id', '=', rec.related_partner_id.id),
                ('related_partner_id', '=', rec.partner_id.id),
            ])
            reciprocal_records |= recp

        # Unlink original
        result = super().unlink()

        # Unlink reciprocals
        # Skip reciprocal calls so we don't trigger an endless loop
        if reciprocal_records:
            reciprocal_records.with_context(skip_reciprocal=True).unlink()

        return result

    def _get_reciprocal_relationship_type(self, rel_type):
        """Return the reciprocal relationship type, if any, for a given type."""
        reciprocal_map = {
        # Parent/child relationships
        'mother': 'child',
        'father': 'child',
        'step_mother': 'step_child',
        'step_father': 'step_child',

        'daughter': 'parent',
        'son': 'parent',
        'step_daughter': 'step_parent',
        'step_son': 'step_parent',

        # Siblings
        'sibling': 'sibling',
        'sibling': 'sibling',
        'half_sibling': 'half_sibling',
        'half_sibling': 'half_sibling',
        'step_sibling': 'step_sibling',
        'step_sibling': 'step_sibling',

        # Spouse relationships
        'spouse': 'spouse',
        'ex_spouse': 'ex_spouse',
        'fiance': 'fiance',

        # Grandparent/grandchild relationships
        'grandmother': 'grandchild',
        'grandfather': 'grandchild',
        'grandchild': 'grandparent',
        'grandson': 'grandparent',

        # Aunts/uncles, nieces/nephews
        'aunt': 'niece/nephew',
        'uncle': 'niece/nephew',
        'niece': 'aunt/uncle',
        'nephew': 'aunt/uncle',

        # Cousins
        'cousin': 'cousin',

        # In-laws
        'father_in_law': 'child_in_law',
        'mother_in_law': 'child_in_law',
        'brother_in_law': 'brother_in_law',  # symmetrical by default
        'sister_in_law': 'sister_in_law',
        'son_in_law': 'parent_in_law',
        'daughter_in_law': 'parent_in_law',
        }
        return reciprocal_map.get(rel_type, False)
