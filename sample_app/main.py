from helpers import *

exit = False

pk = input('Enter your Dwolla public key: ')
sk = input('Enter your Dwolla secret key: ')

while not exit:
    display_options()
    input = get_user_input()
    if input == 'exit':
        exit = True
    else:
        handle_input(input, pk, sk)
