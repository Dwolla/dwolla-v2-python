import json

import dwollav2


def display_options():
    print('Choose from the following actions: ')
    action_menu = '''
    Root (R)
    Retrieve account details (RAD)
    Create account funding source (CAFS)
    Create account VAN (CAVAN)
    List account funding sources (LAFS)
    List and search account transfers (LASAT)
    List account mass payments (LAMP)
    Create receive only customer (CROC)
    Create unverified customer (CUVC)
    Create verified personal customer (CVP)
    Retrieve customer (RC)
    List and search customers (LASC)
    Update customer (UC)
    List customer business classifications (LCBC)
    retrieve business classification (RBC)
    initiate KBA (IKBA)
    retrieve KBA (RKBA)
    verify KBA (VKBA)
    Create beneficial owner (CBO)
    Retrieve beneficial owner (RBO)
    list beneficial owners (LBO)
    update beneficial owner (UBO)
    Remove beneficial owner (DBO)
    Retrieve beneficial ownership status (RBOS)
    Certify beneficial ownership (CBOS)
    Quit (Q)
    '''
    print(action_menu)

def get_user_input():
    return input('Enter your action: ')

def handle_input(input, DWOLLA_APP_KEY, DWOLLA_APP_SECRET):
    client = dwollav2.Client(key = DWOLLA_APP_KEY, secret = DWOLLA_APP_SECRET, environment = 'sandbox')
    application_token = client.Auth.client()
    if input == 'R':
        root(application_token)
    elif input == 'RAD':
        get_account_details(application_token)
    elif input == 'CAFS':
        create_account_funding_source(application_token)
    elif input == 'CAVAN':
        create_account_van(application_token)
    elif input == 'LAFS':
        list_account_funding_sources(application_token)
    elif input == 'LASAT':
        list_and_search_account_transfers(application_token)
    elif input == 'LAMP':
        list_account_mass_payments(application_token)
    elif input == 'CROC':
        create_receive_only_customer(application_token)
    elif input == 'CUVC':
        create_unverified_customer(application_token)
    elif input == 'CVP':
        create_verified_personal_customer(application_token)
    elif input == 'RC':
        retrieve_customer(application_token)
    elif input == 'LASC':
        list_and_search_customers(application_token)
    elif input == 'UC':
        update_customer(application_token)
    elif input == 'LCBC':
        list_customer_business_classifications(application_token)
    elif input == 'RBC':
        retrieve_business_classification(application_token)
    elif input == 'IKBA':
        initiate_kba(application_token)
    elif input == 'RKBA':
        retrieve_kba(application_token)
    elif input == 'VKBA':
        verify_kba(application_token)
    elif input == 'CBO':
        create_beneficial_owner(application_token)
    elif input == 'RBO':
        retrieve_beneficial_owner(application_token)
    elif input == 'LBO':
        list_beneficial_owners(application_token)
    elif input == 'UBO':
        update_beneficial_owner(application_token)
    elif input == 'DBO':
        remove_beneficial_owner(application_token)
    elif input == 'RBOS':
        retrieve_beneficial_ownership_status(application_token)
    elif input == 'CBOS':
        certify_beneficial_ownership(application_token)
    elif input == 'Q':
        quit()


def print_response(res):
    print(json.dumps(res.body, indent = 4))

def print_location(res):
    print(res.headers['Location'])

# ROOT RESOURCE
def root(token):
    res = token.get('/')
    print_response(res)

# ACCOUNT RESOURCE
def get_account_details(token):
    id = input('Enter your account ID: ')
    res = token.get(f'accounts/{id}')
    print_response(res)

def create_account_funding_source(token):
    accountNumber = input('Enter your account number: ')
    routingNumber = input('Enter your routing number: ')
    bankAccountType = input('Enter your bank account type: ')
    name = input('Enter your funding source nickname: ')

    body = {
        'routingNumber': routingNumber,
        'accountNumber': accountNumber,
        'type': bankAccountType,
        'name': name
    }

    res = token.post(f'/funding-sources', body)
    print_location(res)

def create_account_van(token):
    name = input('Enter your account name: ')
    bankAccountType = input('Enter your bank account type: ')

    body = {
        'name': name,
        'type': 'virtual',
        'bankAccountType': bankAccountType
    }

    res = token.post(f'/funding-sources', body)
    print_location(res)

def list_account_funding_sources(token):
    id = input('Enter your account ID: ')
    res = token.get(f'/accounts/{id}/funding-sources')
    print_response(res)

def list_and_search_account_transfers(token):
    id = input('Enter your account ID: ')
    res = token.get(f'/accounts/{id}/transfers')
    print_response(res)

def list_account_mass_payments(token):
    id = input('Enter your account ID: ')
    res = token.get(f'/accounts/{id}/mass-payments')
    print_response(res)

# CUSTOMER RESOURCE
def create_receive_only_customer(token):
    firstName = input('Enter customer first name: ')
    lastName = input('Enter customer last name: ')
    email = input('Enter customer email: ')
    type = 'receive-only'

    body = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'type': type
    }

    res = token.post(f'/customers', body)
    print_location(res)

def create_unverified_customer(token):
    firstName = input('Enter customer first name: ')
    lastName = input('Enter customer last name: ')
    email = input('Enter customer email: ')

    body = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
    }

    res = token.post(f'/customers', body)
    print_location(res)

def create_verified_personal_customer(token):
    firstName = input('Enter customer first name: ')
    lastName = input('Enter customer last name: ')
    email = input('Enter customer email: ')
    address1 = input('Enter customer address 1: ')
    city = input('Enter customer city: ')
    state = input('Enter customer state: ')
    postalCode = input('Enter customer postal code: ')
    dateOfBirth = input('Enter customer date of birth: ')
    ssn = input('Enter customer ssn: ')
    type = 'personal'

    body = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'address1': address1,
        'city': city,
        'state': state,
        'postalCode': postalCode,
        'dateOfBirth': dateOfBirth,
        'ssn': ssn,
        'type': type
    }

    res = token.post(f'/customers', body)
    print_location(res)

def retrieve_customer(token):
    id = input('Enter customer ID: ')
    res = token.get(f'/customers/{id}')
    print_response(res)

def list_and_search_customers(token):
    res = token.get('/customers')
    print_response(res)

def update_customer(token):
    id = input('Enter customer ID: ')
    email = input('Enter updated customer email: ')

    body = {
        'email': email,
    }

    res = token.post(f'/customers/{id}', body)
    print_response(res)

def list_customer_business_classifications(token):
    res = token.get('/business-classifications')
    print_response(res)

def retrieve_business_classification(token):
    id = input('Enter business classification ID: ')
    res = token.get(f'/business-classifications/{id}')
    print_response(res)

# KBA RESOURCE
def initiate_kba(token):
    id = input('Enter customer ID: ')
    res = token.post(f'/customers/{id}/kba')
    print_location(res)

def retrieve_kba(token):
    id = input('Enter KBA session ID: ')
    res = token.get(f'/kba/{id}')
    print_response(res)

def verify_kba(token):
    id = input('Enter KBA session ID: ')

    answers = []
    for i in range(4):
        obj = {}
        question_id = input(f'Enter question ID for question {i+1}: ')
        answer_id = input(f'Enter answer ID for answer {i+1}: ')
        obj['questionId'] = question_id
        obj['answerId'] = answer_id
        answers.append(obj)

    body = {
        'answers': answers
    }

    res = token.post(f'/kba/{id}', body)
    print_response(res)

# BENEFICIAL OWNERS RESOURCE
def create_beneficial_owner(token):
    id = input('Enter customer ID: ')
    firstName = input('Enter beneficial owner first name: ')
    lastName = input('Enter beneficial owner last name: ')
    dateOfBirth = input('Enter beneficial owner date of birth: ')
    ssn = input('Enter beneficial owner ssn: ')
    address1 = input('Enter beneficial owner address 1: ')
    city = input('Enter beneficial owner city: ')
    state = input('Enter beneficial owner state: ')
    country = input('Enter beneficial owner country: ')
    postalCode = input('Enter beneficial owner postal code: ')

    body = {
        'firstName': firstName,
        'lastName': lastName,
        'dateOfBirth': dateOfBirth,
        'ssn': ssn,
        'address': {
            'address1': address1,
            'city': city,
            'stateProvinceRegion': state,
            'country': country,
            'postalCode': postalCode
        }
    }

    res = token.post(f'/customers/{id}/beneficial-owners', body)
    print_location(res)

def retrieve_beneficial_owner(token):
    id = input('Enter beneficial owner ID: ')
    res = token.get(f'/beneficial-owners/{id}')
    print_response(res)

def list_beneficial_owners(token):
    id = input('Enter customer ID: ')
    res = token.get(f'/customers/{id}/beneficial-owners')
    print_response(res)

def update_beneficial_owner(token):
    id = input('Enter beneficial owner ID: ')
    firstName = input('Enter beneficial owner first name: ')
    lastName = input('Enter beneficial owner last name: ')
    dateOfBirth = input('Enter beneficial owner date of birth: ')
    ssn = input('Enter beneficial owner ssn: ')
    address1 = input('Enter beneficial owner address 1: ')
    city = input('Enter beneficial owner city: ')
    state = input('Enter beneficial owner state: ')
    country = input('Enter beneficial owner country: ')
    postalCode = input('Enter beneficial owner postal code: ')

    body = {
        'firstName': firstName,
        'lastName': lastName,
        'dateOfBirth': dateOfBirth,
        'ssn': ssn,
        'address': {
            'address1': address1,
            'city': city,
            'stateProvinceRegion': state,
            'country': country,
            'postalCode': postalCode
        }
    }

    res = token.post(f'/beneficial-owners/{id}', body)
    print_response(res)

def remove_beneficial_owner(token):
    id = input('Enter beneficial owner ID: ')
    res = token.delete(f'/beneficial-owners/{id}')
    print_response(res)

def retrieve_beneficial_ownership_status(token):
    id = input('Enter customer ID: ')
    res = token.get(f'/customers/{id}/beneficial-ownership')
    print_response(res)

def certify_beneficial_ownership(token):
    id = input('Enter customer ID: ')
    body = {
        'status': 'certified'
    }
    res = token.post(f'/customers/{id}/beneficial-ownership', body)
    print_response(res)

