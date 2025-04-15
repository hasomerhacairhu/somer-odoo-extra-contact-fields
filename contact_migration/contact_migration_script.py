import xmlrpc.client
import csv
import base64
import io
import sys
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger('migration_script')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler (logs will be written to 'migration.log')
file_handler = logging.FileHandler('migration.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Define two arrays: one to capture messages from successful try blocks and
# the other for messages from except blocks.
try_logs = []
except_logs = []

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
    msg = "Authentication failed!"
    logger.error(msg)
    except_logs.append(msg)
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

def create_family_relation(parent_id, child_id, relationship_type="child"):
    """Create a family relationship between parent and child."""
    try:
        # Create a family relationship for the given parent-child pair
        models.execute_kw(db, uid, password,
                          'res.partner.family.relation', 'create', [{
                              'partner_id': parent_id,
                              'related_partner_id': child_id,
                              'relationship_type': relationship_type,
                          }])
        msg = f"Created family relation between Parent ID {parent_id} and Child ID {child_id}"
        logger.info(msg)
        try_logs.append(msg)
    except Exception as e:
        msg = f"Failed to create relationship between ID {parent_id} and ID {child_id} due to: {e}"
        logger.error(msg)
        except_logs.append(msg)
        # If creating the family relation fails, delete the partners created in Step 1
        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[parent_id]])
        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[child_id]])
        deletion_msg = f"Deleted partners with ID {parent_id} and ID {child_id}"
        logger.error(deletion_msg)
        except_logs.append(deletion_msg)

def import_contacts(csv_file_path, relation_file_path):
    # Step 1: Import Contacts
    partner_ids_map = {}  # Dictionary to store contactid -> partner_id mapping
    duplicates = {}       # Dictionary to check whether a contact was tried to be created before.
    is_szulo_map = {}     # Maps contactid -> Boolean (True if 'Szulo' in stakeholder, else False)
    
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

            # Check if this contact's stakeholder field contains "Szulo"
            is_szulo_map[row.get('contactid', '')] = ('Szulo' in stakeholder_str)

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

            # Check if the contact already exists before creating it using full name and/or email
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
                    msg = f"Created partner '{full_name}' with ID {partner_id}"
                    logger.info(msg)
                    try_logs.append(msg)
                except Exception as e:
                    msg = f"Failed to create partner '{full_name}' due to error: {e}"
                    logger.error(msg)
                    except_logs.append(msg)
            else:
                # If the partner already exists, use the existing ID
                partner_ids_map[contact_id] = existing_partner[0]
                duplicates[contact_id] = 'duplicate'
                msg = f"Partner '{full_name}' already exists with ID {existing_partner[0]}"
                logger.error(msg)
                except_logs.append(msg)
    
    # Step 2: Create Parent-Child Relationships
    with open(relation_file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Split by the comma to extract parent and child IDs
            relation_data = row.get('crmid,"relcrmid"', '').split(',')
            partner_id_one = relation_data[0]
            partner_id_two = relation_data[1].strip('"')
            # Check if both parent and child contacts exist in partner_ids_map
            if (partner_id_one in partner_ids_map and partner_id_two in partner_ids_map and 
               (duplicates[partner_id_one] != 'duplicate' or duplicates[partner_id_two] != 'duplicate')):
                parent = 0
                child = 0
                if is_szulo_map[partner_id_one] == True:
                    parent = partner_ids_map[partner_id_one]
                    child = partner_ids_map[partner_id_two]
                elif is_szulo_map[partner_id_two] == True:
                    child = partner_ids_map[partner_id_one]
                    parent = partner_ids_map[partner_id_two]

                try:
                    create_family_relation(parent, child)
                except Exception as e:
                    msg = (f"Failed to create relationship between ID {partner_ids_map[partner_id_one]} "
                           f"and ID {partner_ids_map[partner_id_two]} due to error: {e}")
                    logger.error(msg)
                    except_logs.append(msg)
                    # If creating the family relation fails, delete the partners created in Step 1
                    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[partner_ids_map[partner_id_one]]])
                    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[partner_ids_map[partner_id_two]]])
                    del_msg = (f"Deleted partners with ID {partner_ids_map[partner_id_one]} "
                               f"and ID {partner_ids_map[partner_id_two]}")
                    logger.error(del_msg)
                    except_logs.append(del_msg)
            else:
                msg = (f"Relationship error: One or both contacts not found for ID ", 
                       partner_ids_map[partner_id_one], " and ID ", 
                       partner_ids_map[partner_id_two], " "
                       "or partner(s) already exist(s)")
                logger.error(msg)
                except_logs.append(msg)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage_msg = "Usage: {} <contacts_csv_file_path> <relations_csv_file_path>".format(sys.argv[0])
        logger.info(usage_msg)
        try_logs.append(usage_msg)
        sys.exit(1)
    csv_file_path = sys.argv[1]
    relation_file_path = sys.argv[2]
    import_contacts(csv_file_path, relation_file_path)
