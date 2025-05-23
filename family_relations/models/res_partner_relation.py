import json
from odoo import api, fields, models, tools

REL_TYPES_PATH = 'family_relations/data/relationship_types.json'
RECIP_MAP_PATH = 'family_relations/data/reciprocal_map.json'

def load_json_file(path):
    """Utility to load a JSON file from the module."""
    with tools.file_open(path, 'r') as f:
        return json.load(f)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # One2many to store this partner's family relationships
    relation_ids = fields.One2many(
        'res.partner.family.relation',
        'partner_id',
        string='Family Relations'
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

    @api.model
    def _get_relationship_types(self):
        """
        Reads 'relationship_types.json' and returns
        a list of (value, label) pairs for the Selection field.
        """
        return load_json_file(REL_TYPES_PATH)

    relationship_type = fields.Selection(
        selection=lambda self: self._get_relationship_types(),
        string='Relationship',
        required=True,
    )

    comment = fields.Text(
        string='Comment',
        help='Any additional notes or details about this relationship.'
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
                        'comment': record.comment,
                    },
                )

        return record

    def write(self, vals):
        """Override write to update reciprocal records if relationship_type or comment changes."""
        res = super().write(vals)

        fields_that_affect_reciprocal = set(vals.keys()).intersection({'relationship_type', 'comment'})
        if fields_that_affect_reciprocal and not self.env.context.get('skip_reciprocal'):
            for rec in self:
                # Find the reciprocal record on the related partner, if any
                reciprocal_rel = self.search([
                ('partner_id', '=', rec.related_partner_id.id),
                ('related_partner_id', '=', rec.partner_id.id),
                ], limit=1)
                if reciprocal_rel:
                    update_vals = {}
                    if 'relationship_type' in vals:
                        # Compute new reciprocal
                        new_reciprocal_type = rec._get_reciprocal_relationship_type(rec.relationship_type)
                        if new_reciprocal_type:
                            update_vals['relationship_type'] = new_reciprocal_type
                    if 'comment' in vals:
                        # Mirror the new comment
                        update_vals['comment'] = rec.comment

                    if update_vals:
                        reciprocal_rel.with_context(skip_reciprocal=True).write(update_vals)

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
        """
        Return the reciprocal relationship type, if any, for a given type,
        based on 'reciprocal_map.json'.
        """
        reciprocal_map = load_json_file(RECIP_MAP_PATH)
        return reciprocal_map.get(rel_type, False)
