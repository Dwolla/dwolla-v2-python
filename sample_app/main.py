import os
from helpers import *

exit = False

# Get DWOLLA_APP_KEY and DWOLLA_APP_KEY from environment variables
DWOLLA_APP_KEY = os.getenv('DWOLLA_APP_KEY')
DWOLLA_APP_SECRET = os.environ.get('DWOLLA_APP_SECRET')

while not exit:
    display_options()
    input = get_user_input()
    if input == 'exit':
        exit = True
    else:
        handle_input(input, DWOLLA_APP_KEY, DWOLLA_APP_SECRET)
