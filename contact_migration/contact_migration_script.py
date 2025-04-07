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
    Splits the stakeholder_str by '|##|' and returns a list of record IDs
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

def import_contacts(csv_file_path):
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
            try:
                # Create the partner record in Odoo
                partner_id = models.execute_kw(db, uid, password,
                                               'res.partner', 'create', [partner_vals])
                print(f"Created partner with ID {partner_id}")
            except Exception as e:
                print(f"Failed to create partner '{full_name}' due to error: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <csv_file_path>".format(sys.argv[0]))
        sys.exit(1)
    csv_file_path = sys.argv[1]
    import_contacts(csv_file_path)
