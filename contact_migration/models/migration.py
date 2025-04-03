import base64
import csv
import io
from datetime import datetime
from odoo import api, models, fields, _
from odoo.exceptions import UserError

def normalize_date(date_str):
    if not date_str:
        return ''
    # Try to parse with both accepted formats
    for fmt in ("%Y-%m-%d", "%Y.%m.%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # Return the original string if no format matches (or raise an error if preferred)
    return date_str

class ContactImportWizard(models.TransientModel):
    _name = 'contact.import.wizard'
    _description = 'Import Contacts from CSV'

    csv_file = fields.Binary(string="CSV File", required=True, help="Upload your CSV file here")

    def _parse_stakeholder_groups(self, stakeholder_str):
        """
        Splits the stakeholder_str by '|##|' and returns a list of record IDs
        that match (or are created for) each stakeholder name.
        """
        if not stakeholder_str:
            return []
        stakeholder_list = [s.strip() for s in stakeholder_str.split(' |##| ') if s.strip()]

        # If StakeholderGroup references res.partner.category, adjust below accordingly:
        Category = self.env['stakeholder.option']
        cat_ids = []
        for name in stakeholder_list:
            # Search for an existing category with this name
            category = Category.search([('name', '=', name)], limit=1)
            # Create it if not found
            if not category:
                category = Category.create({'name': name})
            cat_ids.append(category.id)
        return cat_ids
    
    def import_contacts(self):
        if not self.csv_file:
            raise UserError(_("Please select a CSV file."))
        # Decode the uploaded file
        file_data = base64.b64decode(self.csv_file)
        # Use io.StringIO to treat it as a text stream
        file_stream = io.StringIO(file_data.decode("utf-8"))
        reader = csv.DictReader(file_stream)

        for row in reader:
            # Combine first and last names to form the full name for Odoo
            first_name = row.get('firstname', '')
            last_name = row.get('lastname', '')
            full_name = f"{first_name} {last_name}".strip()

            # Normalize the date fields to ensure correct format
            birthday = normalize_date(row.get('birthday', ''))
            passport_exp_date = normalize_date(row.get('passport_exp_date', ''))
            
            # Parse the stakeholder field and get the list of option IDs
            stakeholder_str = row.get('stakeholder', '')
            cat_ids = self._parse_stakeholder_groups(stakeholder_str)
           
            # Convert "1" -> True, "0" -> False for boolean fields
            madrich_training = (row.get('madrich_training', '') == '1')
            is_vaccinated = (row.get('vaccinated', '') == '1')
            is_active = (row.get('active', '') == '1')
            
            # Map your CSV columns to Odoo fields
            partner_vals = {
                'name': full_name,
                'email': row.get('email', ''),
                'phone': row.get('phone', ''),
                # Assign the many2many relationship with the list of IDs
                'StakeholderGroup': [(6, 0, cat_ids)],
                'BirthDate': birthday,
                'IDNumber': row.get('id_number', ''),
                'SSN': row.get('soc_sec_nbr', ''),
                'TShirtSize': row.get('size', ''),
                'PlaceOfBirth': row.get('birthplace', ''),
                'TaxID': row.get('tax_id_nbr', ''),
                'PassportNumber': row.get('passport_nbr', ''),
                'PassportExpirationDate': passport_exp_date,
                'BankAccountNumber': row.get('bank_account_nbr', ''),
                'MadrichTraining': madrich_training,
                'IsVaccinated': is_vaccinated,
                'IsActive': is_active
            }
            # Create the contact
            self.env['res.partner'].create(partner_vals)

        return {"type": "ir.actions.act_window_close"}
