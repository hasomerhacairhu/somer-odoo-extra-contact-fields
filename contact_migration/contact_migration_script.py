import xmlrpc.client
import csv
import base64
import io
import sys
from datetime import datetime

# --------------------------
# Destination Configuration
url = 'https://odoodev.somer.hu'
db = 'odoo_dev'
username = 'budapest@hashomerhatzair-eu.com'
password = 'MarciAdrianDev'
# --------------------------

# Connect to Odoo's XML-RPC API
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
if not uid:
    print("Authentication failed!")
    sys.exit(1)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def normalize_date(date_str):
    """
    Normalize a date string from either 'YYYY-MM-DD' or 'YYYY.MM.DD' format
    to 'YYYY-MM-DD'.
    """
    if not date_str:
        return ''
    for fmt in ("%Y-%m-%d", "%Y.%m.%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str

def get_stakeholder_option_ids(stakeholder_str):
    """
    Splits the stakeholder_str by ' |##| ' and returns a list of record IDs
    for the 'stakeholder.option' model. Searches for an existing record
    by name, and creates it if not found.
    """
    if not stakeholder_str:
        return []
    stakeholder_list = [s.strip() for s in stakeholder_str.split(' |##| ') if s.strip()]
    option_ids = []
    for name in stakeholder_list:
        # Search for an existing stakeholder.option record
        res = models.execute_kw(db, uid, password,
                                  'stakeholder.option', 'search',
                                  [[['name', '=', name]]], {'limit': 1})
        if res:
            option_id = res[0]
        else:
            option_id = models.execute_kw(db, uid, password,
                                          'stakeholder.option', 'create',
                                          [{'name': name}])
        option_ids.append(option_id)
    return option_ids

def create_family_relation(parent_id, child_id, relationship_type="parent"):
    """Create a family relationship between parent and child."""
    try:
        # Create a family relationship for the given parent-child pair
        models.execute_kw(db, uid, password,
                          'res.partner.family.relation', 'create', [{
                              'partner_id': parent_id,
                              'related_partner_id': child_id,
                              'relationship_type': relationship_type,
                          }])
        print(f"Created family relation between Parent ID {parent_id} and Child ID {child_id}")
    except Exception as e:
        print(f"Failed to create relationship between Parent ID {parent_id} and Child ID {child_id} due to: {e}")

def import_contacts(csv_file_path, relation_file_path):
    
    # Step 1: Import Contacts
    partner_ids_map = {}  # Dictionary to store contactid -> partner_id mapping
    duplicates = {} # Dictionary to check whether a contact was tried to be created before and if so skip the family relation setup process as well
    with open(csv_file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Combine first and last names for full name
            first_name = row.get('firstname', '')
            last_name = row.get('lastname', '')
            full_name = f"{first_name} {last_name}".strip()

            # Determine Nickname: use provided nickname or default to first_name
            nickname = row.get('nickname', '')
            if not nickname:
                nickname = first_name
            
            # Normalize date fields
            birthday = normalize_date(row.get('birthday', ''))
            passport_exp_date = normalize_date(row.get('passport_exp_date', ''))

            # Process stakeholder field into a list of stakeholder.option IDs
            stakeholder_str = row.get('stakeholder', '')
            option_ids = get_stakeholder_option_ids(stakeholder_str)

            # Convert "1" to True and "0" to False for boolean fields
            madrich_training = (row.get('madrich_training', '') == '1')
            is_vaccinated = (row.get('vaccinated', '') == '1')
            is_active = (row.get('active', '') == '1')

            # Build the partner values dictionary
            partner_vals = {
                'name': full_name,
                'email': row.get('email', ''),
                'phone': row.get('phone', ''),
                'Nickname': nickname,
                'StakeholderGroup': [(6, 0, option_ids)],
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
                'IsActive': is_active,
            }

            contact_id = row.get('contactid', '')
            email = row.get('email', '').strip()
            if email:
                domain = [('name', '=', full_name), ('email', '=', email)]
            else:
                domain = [('name', '=', full_name)]

             # Check if the contact already exists before creating it using full name
            existing_partner = models.execute_kw(db, uid, password,
                    'res.partner', 'search',
                    [domain], {'limit': 1})

            if not existing_partner:
                try:
                    # Create the partner record in Odoo if it doesn't already exist
                    partner_id = models.execute_kw(db, uid, password,
                        'res.partner', 'create', [partner_vals])
                    partner_ids_map[contact_id] = partner_id  # Store the partner ID for this contact
                    duplicates[contact_id] = 'non-duplicate'
                    print(f"Created partner '{full_name}' with ID {partner_id}")
                except Exception as e:
                    print(f"Failed to create partner '{full_name}' due to error: {e}")
            else:
                # If the partner already exists, use the existing ID
                partner_ids_map[contact_id] = existing_partner[0]
                duplicates[contact_id] = 'duplicate'
                print(f"Partner '{full_name}' already exists with ID {existing_partner[0]}")
            
    
    # Step 2: Create Parent-Child Relationships
    with open(relation_file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Split by the comma to extract parent and child IDs
            relation_data = row.get('crmid,"relcrmid"', '').split(',')
            parent_id = relation_data[0]
            child_id = relation_data[1].strip('"')
            # Check if both parent and child contacts exist in partner_ids_map
            if parent_id in partner_ids_map and child_id in partner_ids_map and (duplicates[parent_id] != 'duplicate' or duplicates[child_id] != 'duplicate'):
                parent = partner_ids_map[parent_id]
                child = partner_ids_map[child_id]
                try:
                    create_family_relation(parent, child)
                except Exception as e:
                    print(f"Failed to create relationship between Parent ID {partner_ids_map[parent_id]} and Child ID {partner_ids_map[child_id]}.")
                    # If creating the family relation fails, delete the partner created in Step 1
                    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[parent]])
                    print(f"Deleted partner with ID {parent}")
            else:
                print(f"Relationship error: One or both contacts not found for Parent ID {partner_ids_map[parent_id]} and Child ID {partner_ids_map[child_id]} or partner(s) already exist(s)")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <contacts_csv_file_path> <relations_csv_file_path>".format(sys.argv[0]))
        sys.exit(1)
    csv_file_path = sys.argv[1]
    relation_file_path = sys.argv[2]
    import_contacts(csv_file_path, relation_file_path)
