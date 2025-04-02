import os
import csv
from datetime import datetime
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class ContactMigration(models.TransientModel):
    _name = 'contact.migration'
    _description = 'Migrate contacts from vtiger CSV file'

    def migrate_contacts(self):
        """
        Migrate contacts using a CSV file converted from the vtiger ODS file.
        Log messages are written directly to a file in the module's data folder.
        """
        # Get the module root directory (one level above the "models" folder)
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Define log file path with .txt extension in the module's data folder.
        log_path = os.path.join(module_path, 'data', 'migration_log.txt')
        
        def write_log(message):
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        
        write_log("Starting migration")
        
        # Define CSV file path (assumes you converted your ODS to CSV).
        vtiger_csv_path = os.path.join(module_path, 'data', 'vtiger_contactdetails.csv')
        
        try:
            with open(vtiger_csv_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
            write_log(f"Loaded vtiger CSV file from {vtiger_csv_path} with {len(rows)} rows")
        except Exception as e:
            write_log(f"ERROR reading CSV file: {e}")
            raise UserError(_("Error reading CSV file: %s") % e)
        
        # Define mapping between CSV columns and Odoo res.partner fields.
        field_mapping = {
            'email': 'email',
            'phone': 'phone',
            'stakeholder': 'StakeholderGroup',
            'birthday': 'BirthDate',
            'id_number': 'IDNumber',
            'soc_sec_nbr': 'SSN',
            'size': 'TShirtSize',
            'birthplace': 'PlaceOfBirth',
            'tax_id_nbr': 'TaxID',
            'passport_nbr': 'PassportNumber',
            'passport_exp_date': 'PassportExpirationDate',
            'bank_account_nbr': 'BankAccountNumber',
            'madrich_training': 'MadrichTraining',
            'vaccinated': 'IsVaccinated',
            'active': 'IsActive'
            # Add additional mappings as needed.
        }
        
        for idx, row in enumerate(rows):
            vtiger_id = row.get('contactid')
            if not vtiger_id:
                write_log(f"WARNING: Row {idx} is missing contactid; skipping.")
                continue

            partner_data = {}
            # Combine 'firstname' and 'lastname' into full name.
            first_name = row.get('firstname', '')
            last_name = row.get('lastname', '')
            full_name = f"{first_name} {last_name}".strip()
            partner_data['name'] = full_name

            for src_field, odoo_field in field_mapping.items():
                if src_field in row:
                    partner_data[odoo_field] = row[src_field]
            
            try:
                partner = self.env['res.partner'].create(partner_data)
                write_log(f"Created partner: {partner.name}")
            except Exception as e:
                write_log(f"ERROR creating partner for row {idx}: {e}")
        
        write_log("Migration completed")
        return True
