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
    # Display name of the related partner in the first column:
    related_partner_name = fields.Char(
        string='Contact Name',
        related='related_partner_id.name',
        store=False,
        readonly=True
    )
    # Relationship type selection:
    relationship_type = fields.Selection(
        [
            ('mother', 'Mother'),
            ('father', 'Father'),
            ('step_mother', 'Step-mother'),
            ('step_father', 'Step-father'),
            ('daughter', 'Daughter'),
            ('son', 'Son'),
            ('step_daughter', 'Step-daughter'),
            ('step_son', 'Step-son'),

            ('sister', 'Sister'),
            ('brother', 'Brother'),
            ('half_sister', 'Half-sister'),
            ('half_brother', 'Half-brother'),
            ('step_sister', 'Step-sister'),
            ('step_brother', 'Step-brother'),

            ('spouse', 'Spouse'),
            ('ex_spouse', 'Ex-Spouse'),
            ('fiance', 'Fiancé(e)'),

            ('grandmother', 'Grandmother'),
            ('grandfather', 'Grandfather'),
            ('granddaughter', 'Granddaughter'),
            ('grandson', 'Grandson'),

            ('aunt', 'Aunt'),
            ('uncle', 'Uncle'),
            ('niece', 'Niece'),
            ('nephew', 'Nephew'),

            ('cousin', 'Cousin'),

            ('father_in_law', 'Father-in-law'),
            ('mother_in_law', 'Mother-in-law'),
            ('brother_in_law', 'Brother-in-law'),
            ('sister_in_law', 'Sister-in-law'),
            ('son_in_law', 'Son-in-law'),
            ('daughter_in_law', 'Daughter-in-law')
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
                self.create(
                    {
                        'partner_id': record.related_partner_id.id,
                        'related_partner_id': record.partner_id.id,
                        'relationship_type': reciprocal_type,
                    },
                    # pass context with skip_reciprocal
                    context=dict(self.env.context, skip_reciprocal=True),
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
            'mother': 'daughter',
        'father': 'son',
        'step_mother': 'step_daughter',
        'step_father': 'step_son',

        'daughter': 'mother',
        'son': 'father',
        'step_daughter': 'step_mother',
        'step_son': 'step_father',

        'sister': 'sister',
        'brother': 'brother',
        'half_sister': 'half_sister',
        'half_brother': 'half_brother',
        'step_sister': 'step_sister',
        'step_brother': 'step_brother',

        'spouse': 'spouse',
        'ex_spouse': 'ex_spouse',
        'fiance': 'fiance',

        'grandmother': 'granddaughter',
        'grandfather': 'grandson',
        'granddaughter': 'grandmother',
        'grandson': 'grandfather',

        'aunt': 'niece',
        'uncle': 'nephew',
        'niece': 'aunt',
        'nephew': 'uncle',

        'cousin': 'cousin',

        'father_in_law': 'son_in_law',
        'mother_in_law': 'daughter_in_law',
        'brother_in_law': 'brother_in_law',
        'sister_in_law': 'sister_in_law',
        'son_in_law': 'father_in_law',
        'daughter_in_law': 'mother_in_law'
        }
        return reciprocal_map.get(rel_type, False)
