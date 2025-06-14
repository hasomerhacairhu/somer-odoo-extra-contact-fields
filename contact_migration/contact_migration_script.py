import ssl
import xmlrpc.client
import csv
import base64
import io
import sys
import logging
from datetime import datetime
import json
import os

# Set dry run mode switch
dry_run = False # Set to True for a dry run (simulation), False to apply changes
dry_run_family_relation = {}    # Helps with checking wether a family connection could be succesfully made using dry_run mode

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

# Define two arrays: one to capture messages from try blocks and the other for except blocks.
try_logs = []
except_logs = []



# Connect to Odoo's XML-RPC API only if not in dry run mode.
if not dry_run:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    if not uid:
        msg = "Authentication failed!"
        logger.error(msg)
        except_logs.append(msg)
        sys.exit(1)
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
else:
    # In dry run mode, assign dummy values.
    uid = 1
    models = None  # No API calls will be performed in dry run

def normalize_date(date_str):
    """
    Normalize a date string from either 'YYYY-MM-DD' or 'YYYY.MM.DD' format
    to 'YYYY-MM-DD'.
    """
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y.%m.%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str

def preprocess_row(row):
    """
    Preprocess a row from the CSV file:
    - Replace 'NULL' with None.
    - Normalize date fields.
    """
    processed_row = {}
    for key, value in row.items():
        if value == 'NULL' or value == '':
            processed_row[key] = None  # Replace 'NULL' with None
        elif key in ['passport_exp_date', 'birthday', 'next_birthday']:
            processed_row[key] = normalize_date(value) if value else None
        else:
            processed_row[key] = value.strip() if value else None
    return processed_row

def get_stakeholder_option_ids(stakeholder_str, dry_run=False):
    """
    Splits the stakeholder_str by ' |##| ' and returns a list of record IDs
    for the 'stakeholder.option' model. Searches for an existing record by name,
    and creates it if not found. In dry run mode, dummy IDs are returned.
    """
    if not stakeholder_str:
        return []
    stakeholder_list = [s.strip() for s in stakeholder_str.split(' |##| ') if s.strip()]
    option_ids = []
    for name in stakeholder_list:
        if dry_run:
            msg = f"Dry run: Would create stakeholder.option for '{name}'"
            logger.info(msg)
            try_logs.append(msg)
            dummy_id = f"dry_{name}"
            option_ids.append(dummy_id)
        else:
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

def create_family_relation_parent(parent_id, child_id, relationship_type="child", dry_run=False):
    """Create a family relationship between parent and child."""
    if dry_run:
        msg = f"Dry run: Would create family relation between Parent ID {parent_id} and Child ID {child_id}"
        logger.info(msg)
        try_logs.append(msg)
        return

    try:
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

def create_family_relation_sibling(sibling_id_one, sibling_id_two, relationship_type="sibling", dry_run=False):
    """Create a family relationship between parent and child."""
    if dry_run:
            msg = f"Dry run: Would create family relation between Sibling ID {sibling_id_one} and Sibling ID {sibling_id_two}"
            logger.info(msg)
            try_logs.append(msg)
            return
    try:
        models.execute_kw(db, uid, password,
                          'res.partner.family.relation', 'create', [{
                              'partner_id': sibling_id_one,
                              'related_partner_id': sibling_id_two,
                              'relationship_type': relationship_type,
                          }])
        msg = f"Created family relation between Sibling ID {sibling_id_one} and Sibling ID {sibling_id_two}"
        logger.info(msg)
        try_logs.append(msg)
    except Exception as e:
        msg = f"Failed to create relationship between ID {sibling_id_one} and ID {sibling_id_two} due to: {e}"
        logger.error(msg)
        except_logs.append(msg)
        # If creating the family relation fails, delete the partners created in Step 1
        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[sibling_id_one]])
        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[sibling_id_two]])
        deletion_msg = f"Deleted partners with ID {sibling_id_one} and ID {sibling_id_two}"
        logger.error(deletion_msg)
        except_logs.append(deletion_msg)

def import_contacts(csv_file_path, relation_file_path, map_json_path, dry_run=False):
    # Step 1: Import Contacts
    partner_ids_map = {}  # Maps contactid -> partner_id
    duplicates = {}       # Dictionary to check if a contact was already created
    is_szulo_map = {}     # Maps contactid -> True if "Szülő" in stakeholder field
    country_cache = {}    # Cache to store countries for saving processing power while running the script and avoiding script errors
    state_cache = {}      # Cache to store states/counties for saving processing power while running the script and avoiding script errors
    
    with open(csv_file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = preprocess_row(row)  # Preprocess the row

            # Combine first and last names for full name.
            first_name = row.get('firstname', '')
            last_name = row.get('lastname', '')
            full_name = f"{last_name} {first_name}".strip()

            # Determine nickname: use provided nickname or default to first_name.
            nickname = row.get('nickname', '')
            if not nickname:
                nickname = first_name
            
            # Normalize date fields.
            if not row.get('birthdate') == 'NULL' or None:
                birthday = normalize_date(row.get('birthday', ''))
            else:
                birthday = None
            if not row.get('passport_exp_date') == 'NULL' or None:
                passport_exp_date = normalize_date(row.get('passport_exp_date', ''))
            else:
                passport_exp_date = None

            # Process stakeholder field.
            stakeholder_str = str(row.get('stakeholder', ''))
            option_ids = get_stakeholder_option_ids(stakeholder_str, dry_run=dry_run)
            
            contact_key = row.get('contactid', '')
            is_szulo_map[contact_key] = ('Szülő' in stakeholder_str)

            # Convert string booleans.
            madrich_training = (row.get('madrich_training', '') == '1')
            is_vaccinated = (row.get('vaccinated', '') == '1')
            is_active = (row.get('active', '') == '1')

            state_name = row.get('addresslevel6a', '')
            if state_name not in state_cache:
                state_id = models.execute_kw(db, uid, password,
                'res.country.state', 'search',
                [[['name', '=', state_name]]], {'limit': 1})
                state_cache[state_name] = state_id[0] if state_id else None
            else:
                state_id = state_cache[state_name]
            
            city = row.get('addresslevel5a', '')
            if city == 'NULL':
                city = None
            
            zip = row.get('addresslevel7a', '')
            if zip == 'NULL':
                zip = None
            
            street = row.get('addresslevel8a')
            if street == 'NULL':
                street = None
            
            street2 = row.get('buildingnumbera')
            if street2 == 'NULL':
                street2 = None

            # Get the raw country name from the CSV row
            country_name = row.get('addresslevel1a', None)
            if country_name in (None, 'NULL', ''):
                country_id = None
            else:
                # If not yet in cache, do a search for res.country with name = country_name
                if country_name not in country_cache:
                # In dry_run we don’t actually hit Odoo; just store a dummy ID
                    if dry_run:
                        country_cache[country_name] = f"dry_{country_name}"
                    else:
                        country_search = models.execute_kw(
                        db, uid, password,
                        'res.country', 'search',
                        [[['name', '=', country_name]]],  # look up by exact name
                        {'limit': 1}
                    )
                    country_cache[country_name] = country_search[0] if country_search else None

                country_id = country_cache[country_name]
            

            # Build the partner values dictionary.
            partner_vals = {
                'name': full_name,
                'email': row.get('email', ''),
                'phone': row.get('phone', ''),
                'Nickname': nickname,
                'country_id': country_id,
                'state_id': state_id,
                'city': city,
                'zip': zip,
                'street': street,
                'street2': street2,
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
            email_field = row.get('email', '')
            if email_field:
                domain = [('name', '=', full_name), ('email', '=', email_field)]
            else:
                domain = [('name', '=', full_name)]

            # In dry run mode, simulate that no partner exists.
            if not dry_run:
                existing_partner = models.execute_kw(db, uid, password,
                    'res.partner', 'search', [domain], {'limit': 1})
            else:
                existing_partner = []

            if not existing_partner:
                if dry_run:
                    dummy_partner_id = f"{contact_id}"
                    partner_ids_map[contact_id] = dummy_partner_id
                    dry_run_family_relation[contact_id] = dummy_partner_id
                    duplicates[contact_id] = 'non-duplicate'
                    msg = f"Dry run: Would create partner '{full_name}' with dummy ID {dummy_partner_id}"
                    logger.info(msg)
                    try_logs.append(msg)
                else:
                    try:
                        partner_id = models.execute_kw(db, uid, password,
                                                       'res.partner', 'create', [partner_vals])
                        partner_ids_map[contact_id] = partner_id
                        duplicates[contact_id] = 'non-duplicate'
                        msg = f"Created partner '{full_name}' with ID {partner_id}"
                        logger.info(msg)
                        try_logs.append(msg)
                    except Exception as e:
                        msg = f"Failed to create partner '{full_name}' due to error: {e}"
                        logger.error(msg)
                        except_logs.append(msg)
            else:
                partner_ids_map[contact_id] = existing_partner[0]
                duplicates[contact_id] = 'duplicate'
                msg = f"Partner '{full_name}' already exists with ID {existing_partner[0]}"
                logger.info(msg)
                try_logs.append(msg)

    # JSON: After the for loop, write the maps out to JSON
    try:
        with open(map_json_path, 'w', encoding='utf-8') as jf:
            json.dump({
                'partner_ids_map': partner_ids_map,
                'duplicates': duplicates,
                'is_szulo_map': is_szulo_map,
            }, jf, ensure_ascii=False, indent=4)
        logger.info(f"JSON file successfully saved to {map_json_path}")
    except Exception as e:
        logger.error(f"Error saving JSON file: {e}")
    
    # Step 2: Create Parent-Child Relationships

    # JSON: Load the full JSON file back into memory
    try:
        with open(map_json_path, 'r', encoding='utf-8') as jf:
            stored = json.load(jf)
            partner_ids_map = stored.get('partner_ids_map', {})
            duplicates = stored.get('duplicates', {})
            is_szulo_map = stored.get('is_szulo_map', {})
    except FileNotFoundError:
        logger.error(f"Mapping JSON file not found at {map_json_path}; cannot build relations.")
        return
    except Exception as e:
        logger.error(f"Error loading mapping JSON file: {e}")
        return
    
    with open(relation_file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            partner_id_one = row.get('crmid', '').strip('"')
            partner_id_two = row.get('relcrmid', '').strip('"')
            if not partner_id_one or not partner_id_two:
                logger.warning(f"Skipping malformed row: {row}")
                continue  # Skip this row if either value is missing

            if (partner_id_one in partner_ids_map and partner_id_two in partner_ids_map and 
               (duplicates[partner_id_one] != 'duplicate' or duplicates[partner_id_two] != 'duplicate')):
                parent = 0
                child = 0
                if is_szulo_map[partner_id_one]:
                    parent = partner_ids_map[partner_id_one]
                    child = partner_ids_map[partner_id_two]
                elif is_szulo_map[partner_id_two]:
                    child = partner_ids_map[partner_id_one]
                    parent = partner_ids_map[partner_id_two]
                # If there is no parent, automatically resort to sibling relation
                else:
                    sibling_one = partner_ids_map[partner_id_one]
                    sibling_two = partner_ids_map[partner_id_two]
                    try:
                        create_family_relation_sibling(sibling_one, sibling_two, dry_run=dry_run)
                    except Exception as e:
                        msg = (f"Failed to create relationship between ID {partner_ids_map[partner_id_one]} "
                           f"and ID {partner_ids_map[partner_id_two]} due to error: {e}")
                        logger.error(msg)
                        except_logs.append(msg)
                        if not dry_run:
                            models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[partner_ids_map[partner_id_one]]])
                            models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[partner_ids_map[partner_id_two]]])
                            del_msg = (f"Deleted partners with ID {partner_ids_map[partner_id_one]} "
                                   f"and ID {partner_ids_map[partner_id_two]}")
                            logger.error(del_msg)
                            except_logs.append(del_msg)

                try:
                    if parent and child:
                        create_family_relation_parent(parent, child, dry_run=dry_run)
                except Exception as e:
                    msg = (f"Failed to create relationship between ID {partner_ids_map[partner_id_one]} "
                           f"and ID {partner_ids_map[partner_id_two]} due to error: {e}")
                    logger.error(msg)
                    except_logs.append(msg)
                    if not dry_run:
                        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[partner_ids_map[partner_id_one]]])
                        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[partner_ids_map[partner_id_two]]])
                        del_msg = (f"Deleted partners with ID {partner_ids_map[partner_id_one]} "
                                   f"and ID {partner_ids_map[partner_id_two]}")
                        logger.error(del_msg)
                        except_logs.append(del_msg)
            else:
                msg = (f"Relationship error: One or both contacts not found for IDs "
                       f"{partner_ids_map[partner_id_one]} and {partner_ids_map[partner_id_two]}"
                       " or partner(s) already exist(s)")
                logger.error(msg)
                except_logs.append(msg)

    # JSON: Write the updated maps back to the JSON file to keep file & memory in sync
    try:
        with open(map_json_path, 'w', encoding='utf-8') as jf:
            json.dump({
                'partner_ids_map': partner_ids_map,
                'duplicates':       duplicates,
                'is_szulo_map':     is_szulo_map,
            }, jf, ensure_ascii=False, indent=4)
        logger.info(f"Updated mapping JSON file saved to {map_json_path}")
    except Exception as e:
        logger.error(f"Error saving updated mapping JSON file: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage_msg = "Usage: {} <contacts_csv_file_path> <relations_csv_file_path> <map_json_output_path>".format(sys.argv[0])
        logger.info(usage_msg)
        try_logs.append(usage_msg)
        sys.exit(1)
    csv_file_path = sys.argv[1]
    relation_file_path = sys.argv[2]
    map_json_path = sys.argv[3]
    import_contacts(csv_file_path, relation_file_path, map_json_path, dry_run=dry_run)
