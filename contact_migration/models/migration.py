import os
import pandas as pd
import logging
from datetime import datetime
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class ContactMigration(models.TransientModel):
    _name = 'contact.migration'
    _description = 'Migrate contacts from Yetiforce CSV and vtiger ODS files'

    def migrate_contacts(self):
        """
        Migrate contacts using CSV and ODS files from the module's data folder.
        """
        # Get the module root directory (one level above the "models" folder)
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Define file paths relative to the module's data folder
        yetiforce_csv_path = os.path.join(module_path, 'data', 'u_yf_contacts_contacts.csv')
        vtiger_ods_path = os.path.join(module_path, 'data', 'vtiger_contactdetails.ods')
        
        try:
            contacts_df = pd.read_csv(yetiforce_csv_path)
            logging.info("Loaded Yetiforce CSV file successfully from %s", yetiforce_csv_path)
        except Exception as e:
            raise UserError(_("Error reading CSV file: %s") % e)

        try:
            # Use the 'odf' engine for ODS files
            relationships_df = pd.read_excel(vtiger_ods_path, engine='odf')
            logging.info("Loaded vtiger ODS file successfully from %s", vtiger_ods_path)
        except Exception as e:
            logging.warning("Error reading ODS file: %s", e)
            relationships_df = None

        # Define mapping between CSV columns and Odoo res.partner fields
        field_mapping = {
            'contact_name': 'name',
            'email_address': 'email',
            'phone_number': 'phone',
            # Add additional mappings as needed
        }

        # Process contacts from CSV
        for idx, row in contacts_df.iterrows():
            partner_data = {}
            for src_field, odoo_field in field_mapping.items():
                if src_field in row:
                    partner_data[odoo_field] = row[src_field]
            
            # Example: Convert date strings to date objects for EntryDate
            if 'EntryDate' in partner_data and isinstance(partner_data['EntryDate'], str):
                try:
                    partner_data['EntryDate'] = datetime.strptime(partner_data['EntryDate'], '%Y-%m-%d').date()
                except Exception as e:
                    logging.warning("Date conversion error on row %s: %s", idx, e)
            
            try:
                partner = self.env['res.partner'].create(partner_data)
                logging.info("Created partner: %s", partner.name)
            except Exception as e:
                logging.error("Error creating partner for row %s: %s", idx, e)

        # Optionally, process relationships from the ODS file
        if relationships_df is not None:
            relationship_mapping = {
                'MainContact': 'partner_id',
                'RelatedContact': 'related_partner_id',
                'RelationType': 'relationship_type',
                'RelationComment': 'comment'
            }
            for idx, row in relationships_df.iterrows():
                relation_vals = {}
                for src_field, odoo_field in relationship_mapping.items():
                    if src_field in row:
                        relation_vals[odoo_field] = row[src_field]
                
                # Additional logic might be needed here to resolve partner IDs,
                # such as searching for a partner by name.
                try:
                    self.env['res.partner.family.relation'].create(relation_vals)
                    logging.info("Created family relation record.")
                except Exception as e:
                    logging.error("Error creating family relation for row %s: %s", idx, e)

        return True
